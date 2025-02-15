

# Create your views here.
from django.shortcuts import render
from .models import Post

def home(request):
    posts = Post.objects.all()
    return render(request, 'forum/home.html', {'posts': posts})
