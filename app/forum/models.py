

from django.db import models
from django.contrib.auth.models import User

def get_default_user():
    return User.objects.get_or_create(username='default_user')[0].id

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.title}"