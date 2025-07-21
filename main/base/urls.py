from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('login',views.loginUser,name="login"),
    path('register',views.registerUser,name="register"),
    path('logout',views.logoutUser,name="logout"),
    
    path('<str:username>',views.get_conversation,name="getConversation"),
    path('c/create',views.create_conversation,name="createConversation"),
    path('c/update/<int:conversation_id>',views.update_conversation,name="updateConversation"),
    path('c/delete/<int:conversation_id>',views.delete_conversation,name="deleteConversation"),
    path('c/<str:username>/send',views.save_message,name="message"),
    path('c/message/delete/<int:message_id>',views.delete_message,name="deleteMessage")
]
