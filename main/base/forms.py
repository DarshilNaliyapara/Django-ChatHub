from django.forms import ModelForm
from .models import Conversation, Message
from django import forms


class ConversationForm(ModelForm):
    class Meta:
        model = Conversation
        fields = ["conversation_name", "conversation_username", "conversation_about"]
        widgets = {
            "conversation_name": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2 rounded-lg bg-gray-700 text-white border border-gray-600",
                    "placeholder": "Enter conversation name",
                }
            ),
            "conversation_username": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2 rounded-lg bg-gray-700 text-white border border-gray-600",
                    "placeholder": "Enter conversation username",
                }
            ),
            "conversation_about": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-2 rounded-lg bg-gray-700 text-white border border-gray-600",
                    "placeholder": "About this conversation",
                    "rows": 4,
                }
            ),
        }


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["body"]
        labels = {
            "body": "",  # This hides the label
        }
        widgets = {
            "body": forms.TextInput(
                attrs={
                    "autofocus": "autofocus",
                    "class": "flex-1 p-2 mt-1 rounded-full w-full bg-zinc-900 text-white border border-gray-600 focus:outline",
                    "placeholder": "Type a message...",
                }
            )
        }
