from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, create_post, signup, posts_view, messaging_view

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('create/', create_post, name='create_post'),
    path('posts/', posts_view, name='posts'),
    path('messaging/', messaging_view, name='messaging'),

    # Authentication Routes
    path('login/', auth_views.LoginView.as_view(template_name='forum/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
