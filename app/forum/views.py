from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post

@login_required  # User must be logged in to submit a post
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Post.objects.create(user=request.user, title=title, content=content)
        return redirect('home')  # Redirect to homepage after submitting

    return render(request, 'forum/create_post.html')
