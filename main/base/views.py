from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.db.models import OuterRef, Subquery, Q
from django.http import HttpResponse, JsonResponse
from .models import Conversation, Message
from .forms import ConversationForm, MessageForm
import re


def registerUser(request):

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username").lower()
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if username:
            user = User.objects.filter(username=username).first()
            if user:
                messages.error(request, "This username is already taken")

            if password1 != password2:
                messages.error(request, "Password does not match")

            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password1,  # Automatically hashed
            )

            if new_user:
                login(request, new_user)
                return redirect("index")
            else:
                messages.error(request, "Error occurred during user registration!")
                return redirect("index")

    context = {}
    return render(request, "auth/register.html", context)


def loginUser(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not Exsist!!")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Username or password incorrect!")
    context = {}
    return render(request, "auth/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def index(request):

    query = request.GET.get("q", "")

    # Step 1: Subquery to get latest message ID per conversation
    latest_message_subquery = (
        Message.objects.filter(conversation=OuterRef("pk"))
        .order_by("-created_at")
        .values("id")[:1]
    )

    # Step 2: Annotate conversations with latest message ID

    if query:
        conversations_query = Conversation.objects.annotate(
            latest_message_id=Subquery(latest_message_subquery)
        ).filter(
            Q(conversation_username__icontains=query)
            | Q(conversation_name__icontains=query)
        )
    else:
        conversations_query = Conversation.objects.annotate(
            latest_message_id=Subquery(latest_message_subquery)
        ).filter(participants=request.user)

    conversations = list(conversations_query.order_by("-latest_message_id"))

    # Step 3: Pull all related messages using those IDs
    message_ids = [c.latest_message_id for c in conversations if c.latest_message_id]
    latest_messages = Message.objects.filter(id__in=message_ids).select_related(
        "user", "conversation"
    )

    # Step 4: Create a map and attach directly
    message_map = {m.conversation_id: m for m in latest_messages}
    for c in conversations:
        c.latest_message = message_map.get(c.id)

    return render(
        request,
        "index.html",
        {
            "conversations": conversations,
            "user": request.user,
        },
    )


@login_required(login_url="login")
def get_conversation(request, username):

    conversation = get_object_or_404(Conversation, conversation_username=username)
    form = MessageForm()
    conversation_messages = conversation.message_set.all().order_by("-created_at")
    # Step 1: Subquery to get latest message ID per conversation
    latest_message_subquery = (
        Message.objects.filter(conversation=OuterRef("pk"))
        .order_by("-created_at")
        .values("id")[:1]
    )

    # Step 2: Annotate conversations with latest message ID
    conversations = list(
        Conversation.objects.annotate(
            latest_message_id=Subquery(latest_message_subquery)
        )
        .filter(participants=request.user)
        .order_by("-latest_message_id")
    )

    # Step 3: Pull all related messages using those IDs
    message_ids = [c.latest_message_id for c in conversations if c.latest_message_id]
    latest_messages = Message.objects.filter(id__in=message_ids).select_related(
        "user", "conversation"
    )

    # Step 4: Create a map and attach directly
    message_map = {m.conversation_id: m for m in latest_messages}
    for c in conversations:
        c.latest_message = message_map.get(c.id)

    participants = conversation.participants.all()
    return render(
        request,
        "conversation.html",
        {
            "conversation": conversation,
            "participants": participants,
            "conversation_messages": conversation_messages,
            "conversations": conversations,
            "user": request.user,
            "form": form,
        },
    )


@login_required(login_url="login")
def create_conversation(request):
    form = ConversationForm()
    if request.method == "POST":
        form = ConversationForm(request.POST)
        if form.is_valid():
            conversation = form.save(commit=False)
            conversation.admin = request.user
            if not conversation.conversation_username:
                conversation.conversation_username = re.sub(
                    r"[^a-z0-9]", "", conversation.conversation_name.lower()
                )
            conversation.save()
            conversation.participants.add(request.user)
            return redirect("index")
    context = {"form": form}
    return render(request, "conversation_form.html", context)


@login_required(login_url="login")
def update_conversation(request, conversation_id):
    conversation = Conversation.objects.get(id=conversation_id)
    form = ConversationForm(instance=conversation)
    if request.user != conversation.admin:
        return HttpResponse("Unauthorize access!!", 401)
    if request.method == "POST":
        form = ConversationForm(request.POST, instance=conversation)
        if form.is_valid():
            conversation = form.save(commit=False)
            if not conversation.conversation_username:
                conversation.conversation_username = (
                    conversation.conversation_name.lower().replace(" ", "")
                )
            conversation.save()
            return redirect("index")
    context = {"form": form}
    return render(request, "conversation_form.html", context)


@login_required(login_url="login")
def delete_conversation(request, conversation_id):
    if request.method == "POST":
        conversation = Conversation.objects.get(id=conversation_id)
        if conversation:
            conversation.delete()
            return redirect("index")
        else:
            messages.error(request, "Conversation not found")


@login_required(login_url="login")
def save_message(request, username):
    if request.method == "POST":
        form = MessageForm(request.POST)
        conversation = Conversation.objects.get(conversation_username=username)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.user = request.user
            conversation.participants.add(request.user)
            message.save()
            return redirect("getConversation", username=username)


@login_required(login_url="login")
def delete_message(request, message_id):
    if request.method == "POST":
        message = get_object_or_404(Message, id=message_id)

        if message.user == request.user or request.user.is_staff:
            message.delete()
            return JsonResponse({"status": "success"})
        else:
            return HttpResponseForbidden("You are not allowed to delete this message.")

    return JsonResponse({"error": "Invalid request method"}, status=400)
