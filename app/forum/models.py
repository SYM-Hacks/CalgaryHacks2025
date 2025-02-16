from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def get_default_user():
    return User.objects.first().id if User.objects.exists() else None

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

def get_default_category():
    # Now that Category is defined, this function safely creates or retrieves the 'General' category.
    category, created = Category.objects.get_or_create(name='General')
    return category.id

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=get_default_category)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # New field for post image
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.category.name}"


class Chat(models.Model):
    user1 = models.ForeignKey(User, related_name='chats_as_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='chats_as_user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def get_other_user(self, current_user):
        """Returns the other participant in the chat."""
        return self.user2 if self.user1 == current_user else self.user1

    def __str__(self):
        return f"Chat between {self.user1} and {self.user2}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE, null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='message_images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content or '[Image]'}"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # a user can only like a post once

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"
