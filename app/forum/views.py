from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Post
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'forum/signup.html', {'form': form})

@login_required  # User must be logged in to submit a post

def home(request):
    posts = Post.objects.all()
    return render(request, 'forum/home.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Post.objects.create(user=request.user, title=title, content=content)

        return redirect('home')  # Redirect to homepage after submitting


        return redirect('/')
    return render(request, 'forum/create_post.html')
