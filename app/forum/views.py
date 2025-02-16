from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Category,Message
import json





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

    if category_filter:
        posts = Post.objects.filter(category__name=category_filter)
    else:
        posts = Post.objects.all()

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
            return redirect('home')

    categories = Category.objects.all()
    return render(request, 'forum/create_post.html', {'categories': categories})



@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')

        # Check if the category exists before assigning it
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None

        if category:
            Post.objects.create(user=request.user, title=title, content=content, category=category)
            return redirect('home')

    categories = Category.objects.all()
    return render(request, 'forum/create_post.html', {'categories': categories})

@login_required
def posts_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        author = request.user  # Ensure author is assigned

        if title and content:
            Post.objects.create(title=title, content=content, author=author)

        return redirect("posts")  # Redirect after poçsting

    # Fetch all posts to display
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "forum/posts.html", {"posts": posts})



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
    # You can pass additional context if needed, here we're just using request.user
    return render(request, 'forum/profile.html')

@login_required
def update_bio_view(request):
    if request.method == "POST":
        new_bio = request.POST.get('bio', '')
        # Save the new bio; for example, if using a Profile model linked to User:
        profile = request.user.profile  # Adjust according to your implementation
        profile.bio = new_bio
        profile.save()
    return redirect('profile')
