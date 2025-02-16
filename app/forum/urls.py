from django.urls import path
from .views import home, create_post, signup, login_view, logout_view, posts_view, messaging_view

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create/', create_post, name='create_post'),
    path('posts/', posts_view, name='posts'),  
    path('messages/', messaging_view, name='messages'),  
]
