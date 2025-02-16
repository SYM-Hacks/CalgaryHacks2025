from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def get_default_user():
    return User.objects.first().id  # Use the first user in the database


def get_default_category():
    return Category.objects.get_or_create(name='General')[0].id  # Returns only the ID

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=get_default_category)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)

    def __str__(self):
        return self.title

class Chat(models.Model):
    user1 = models.ForeignKey(User, related_name='chats_as_user1', on_delete=models.CASCADE, null=False, blank=False)
    user2 = models.ForeignKey(User, related_name='chats_as_user2', on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)

    def get_other_user(self, current_user):
        """Returns the other participant in the chat."""
        return self.user2 if self.user1 == current_user else self.user1

    def __str__(self):
        return f"Chat between {self.user1} and {self.user2}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
