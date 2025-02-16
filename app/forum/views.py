from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Category,Message,Profile
import json
from django.contrib.auth.models import User




def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in after signup
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'forum/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home(request):
    category_filter = request.GET.get('category', None)

    # Get admin users (staff or superusers)
    admin_users = User.objects.filter(is_staff=True)  # Only staff/admin users

    # Filter posts by admin users
    if category_filter:
        posts = Post.objects.filter(user__in=admin_users, category__name=category_filter)
    else:
        posts = Post.objects.filter(user__in=admin_users)  # Only admin posts

    categories = Category.objects.all()
    return render(request, 'forum/home.html', {'posts': posts, 'categories': categories})

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None

        if category:
            Post.objects.create(user=request.user, title=title, content=content, category=category)
            return redirect('posts')

    categories = Category.objects.all()
    return render(request, 'forum/post.html', {'categories': categories})



@login_required
def posts_view(request):
    categories = Category.objects.all()
    category_filter = request.GET.get('category')
    if category_filter:
        posts = Post.objects.filter(category__name=category_filter).order_by("-created_at")
    else:
        posts = Post.objects.all().order_by("-created_at")
    return render(request, "forum/posts.html", {"posts": posts, "categories": categories})




@login_required
def messaging_view(request):
    """View for the messaging page"""
    messages = Message.objects.all().order_by('timestamp')  # Get messages ordered by time
    return render(request, 'forum/messaging.html', {'messages': messages})

@login_required
def get_messages(request):
    """Return recent messages as JSON"""
    messages = Message.objects.all().order_by('timestamp')
    message_data = [{"sender": msg.sender.username, "content": msg.content} for msg in messages]
    return JsonResponse({"messages": message_data})

@csrf_exempt
@login_required
def send_message(request):
    """Handle new message submissions"""
    if request.method == "POST":
        data = json.loads(request.body)
        message_content = data.get("message", "").strip()

        if message_content:
            message = Message.objects.create(sender=request.user, content=message_content)
            return JsonResponse({"status": "success", "message": message.content})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'forum/profile.html', {'bio': profile.bio})


@login_required
def update_bio_view(request):
    if request.method == "POST":
        new_bio = request.POST.get('bio', '').strip()
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.bio = new_bio  # Assign the new bio
        profile.save()
    return redirect('profile')
