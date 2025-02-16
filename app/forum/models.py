from django.db import models
from django.contrib.auth.models import User

def get_default_user():
    return User.objects.get_or_create(username='default_user')[0].id

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to User
    timestamp = models.DateTimeField(auto_now_add=True)  # Auto add timestamp
    
    def __str__(self):
        return self.title

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content}"   
