from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Profile, Chat, Message, Post, Category, Like, Follow, Comment, FinancialEntry
import json
from django.contrib.auth.models import User
from django.utils import timezone
import pytz
from .forms import ProfilePictureForm, FinancialEntryForm


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
        posts = Post.objects.filter(user__in=admin_users).order_by('-created_at')

    categories = Category.objects.all()
    return render(request, 'forum/home.html', {'posts': posts, 'categories': categories})

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')  # Get the uploaded image if provided

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None

        if category:
            Post.objects.create(
                user=request.user,
                title=title,
                content=content,
                category=category,
                image=image  # Save the image (or None if not provided)
            )
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

    # For each post, determine if the current user has liked it
    for p in posts:
        p.has_liked = p.like_set.filter(user=request.user).exists()


    return render(request, "forum/posts.html", {"posts": posts, "categories": categories})


@login_required
def messaging_view(request):
    """View for the messaging page"""
    messages = Message.objects.all().order_by('timestamp')  # Get messages ordered by time
    return render(request, 'forum/messaging.html', {'messages': messages})

@login_required
def get_messages(request):
    chat_id = request.GET.get('chat_id')
    chat = get_object_or_404(Chat, id=chat_id)
    messages = chat.messages.all().order_by('timestamp')
    
    mountain_tz = pytz.timezone("America/Denver")
    message_data = []
    for msg in messages:
        msg_data = {
            "id": msg.id,  # So we can track the last message
            "sender": msg.sender.username,
            "content": msg.content,
            "timestamp": timezone.localtime(msg.timestamp, mountain_tz).strftime("%Y-%m-%d %H:%M:%S"),
            "image": msg.image.url if msg.image else ""
        }
        message_data.append(msg_data)
    
    return JsonResponse({"messages": message_data})




@login_required
def send_message(request, chat_id):
    if request.method == "POST":
        chat = get_object_or_404(Chat, id=chat_id)
        content = request.POST.get("message", "").strip()
        image = request.FILES.get("image")  # Retrieve the uploaded image, if any
        
        # Debug: Uncomment the next line to see what files are being uploaded.
        # print("Uploaded files:", request.FILES)
        
        if content or image:
            Message.objects.create(
                chat=chat,
                sender=request.user,
                content=content,
                image=image
            )
        return redirect("chat_detail", chat_id=chat.id)
    return redirect("chat_detail", chat_id=chat.id)



@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'forum/profile.html', {
        'profile': profile,
        'bio': profile.bio,
    })



@login_required
def update_bio_view(request):
    if request.method == "POST":
        new_bio = request.POST.get('bio', '').strip()
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.bio = new_bio  # Assign the new bio
        profile.save()
    return redirect('profile')


@login_required
def chat_list(request):
    # Get all chats where the current user is either user1 or user2
    chats = Chat.objects.filter(user1=request.user) | Chat.objects.filter(user2=request.user)

    # Attach the "other_user" attribute to each chat
    for chat in chats:
        chat.other_user = chat.get_other_user(request.user)

    return render(request, "chat_list.html", {"chats": chats})

@login_required
def get_or_create_chat(request, user_id):
    user2 = get_object_or_404(User, id=user_id)

    # Ensure we don't create duplicate chats
    chat = Chat.objects.filter(user1=request.user, user2=user2).first() or \
           Chat.objects.filter(user1=user2, user2=request.user).first()

    if not chat:
        chat = Chat.objects.create(user1=request.user, user2=user2)

    return redirect("chat_detail", chat_id=chat.id)


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user not in [chat.user1, chat.user2]:
        return redirect("messages")
    messages = chat.messages.all().order_by("timestamp")
    if request.method == "POST":
        content = request.POST.get("message", "").strip()
        if content:
            Message.objects.create(chat=chat, sender=request.user, content=content)
        return redirect("chat_detail", chat_id=chat.id)
    return render(request, "chat_detail.html", {
        "chat": chat,
        "messages": messages,
        "other_user": chat.get_other_user(request.user),
    })

@login_required
def messages_view(request, user_id=None):
    if user_id:
        # Get or create a chat between two users
        other_user = get_object_or_404(User, id=user_id)
        chat, created = Chat.objects.get_or_create(
            participants__in=[request.user, other_user],
            defaults={"name": None},
        )
        chat.participants.add(request.user, other_user)  # Ensure both users are in chat
    else:
        chat = None

    chats = request.user.chats.all()  # Get all chats for user
    return render(request, "forum/messages.html", {"chats": chats, "active_chat": chat})

@login_required
def user_list(request):
    # Exclude the currently logged-in user, so they only see others
    users = User.objects.exclude(id=request.user.id)
    return render(request, "forum/user_list.html", {"users": users})


@login_required
def create_chat_view(request):
    if request.method == "GET":
        # Show a form to select another user
        users = User.objects.exclude(id=request.user.id)
        return render(request, "create_chat.html", {"users": users})

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        other_user = get_object_or_404(User, id=user_id)

        # Check if chat already exists for these two users
        chat = Chat.objects.filter(
            user1__in=[request.user, other_user],
            user2__in=[request.user, other_user]
        ).first()

        if not chat:
            # If no existing chat, create a new one
            chat = Chat.objects.create(user1=request.user, user2=other_user)

        # Redirect to the chat_detail page
        return redirect("chat_detail", chat_id=chat.id)

@login_required
def user_profile(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    profile, created = Profile.objects.get_or_create(user=user_obj)

    # If Follow model is:
    # follower = models.ForeignKey(User, related_name='following')
    # followed = models.ForeignKey(User, related_name='followers')
    # Then to check if request.user is following user_obj:
    is_following = False
    if request.user.is_authenticated and user_obj != request.user:
        is_following = Follow.objects.filter(follower=request.user, followed=user_obj).exists()

    return render(
        request, 
        'forum/user_profile.html', 
        {
            'user_obj': user_obj,
            'profile': profile,
            'is_following': is_following,
        }
    )


@login_required
def update_profile_picture(request):
    # Get or create the profile for the current user
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # or wherever you want to redirect
    else:
        form = ProfilePictureForm(instance=profile)
    return render(request, "forum/update_profile_picture.html", {"form": form})

@login_required
def test_upload(request):
    if request.method == "POST":
        print("Uploaded files:", request.FILES)  # Check your console for output
        return redirect("home")
    return render(request, "forum/test_upload.html")

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        # If the like already exists, it means user is "unliking" the post
        like.delete()
    return redirect('posts')  # or wherever you want to redirect

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if user_to_follow == request.user:
        return redirect('home')  # Can't follow yourself, or handle error
    
    follow_obj, created = Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
    if not created:
        # Unfollow if it already existed
        follow_obj.delete()
    return redirect('user_profile', user_id=user_to_follow.id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        content = request.POST.get("comment")
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
    return redirect("posts")

@login_required
def tips_view(request):
    craving = request.GET.get('craving', '')
    recipes = []
    if craving:
        recipes = [
            {'title': f'{craving.title()} Delight', 'url': 'https://example.com/recipe1'},
            {'title': f'Easy {craving.title()}', 'url': 'https://example.com/recipe2'},
            {'title': f'{craving.title()} Special', 'url': 'https://example.com/recipe3'},
        ]
    return render(request, 'forum/tips.html', {'recipes': recipes})


@login_required
def finance_manager(request):
    if request.method == 'POST':
        form = FinancialEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('finance_manager')
    else:
        form = FinancialEntryForm()
    # Get current user's entries, most recent first
    entries = FinancialEntry.objects.filter(user=request.user).order_by('-date')
    # Compute summary totals
    total_income = sum(entry.amount for entry in entries if entry.entry_type == 'income')
    total_expense = sum(entry.amount for entry in entries if entry.entry_type == 'expense')
    balance = total_income - total_expense

    return render(request, 'forum/finance_manager.html', {
        'form': form,
        'entries': entries,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
    })
