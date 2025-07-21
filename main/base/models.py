from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Conversation(models.Model):
    admin = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    conversation_name = models.CharField(max_length=100)
    conversation_username = models.CharField(max_length=100,unique=True,null=True,blank=True)
    conversation_about = models.TextField(null=True,blank=True)
    participants = models.ManyToManyField(User,related_name="participants",blank=True)
    is_group = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated_at','-created_at']
    
    def __str__(self):
        return self.conversation_name
    
class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    conversation = models.ForeignKey(Conversation,on_delete=models.CASCADE,blank=True)
    body = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.body[0:50]
    