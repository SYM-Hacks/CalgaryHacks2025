from django.urls import path
from .views import home, signup, login_view, logout_view, posts_view, profile_view, user_list, chat_list, create_post, update_bio_view
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('posts/', posts_view, name='posts'),
    path('profile/', profile_view, name='profile'),
    path("messages/", views.chat_list, name="messages"),
    path("chats/<int:chat_id>/", views.chat_detail, name="chat_detail"),
    path("chats/new/", views.create_chat_view, name="create_chat"),
    path("chats/<int:chat_id>/send/", views.send_message, name="send_message"),
    path("users/", user_list, name="user_list"),
    path("chats/", chat_list, name="chat_list"),
    path("messages/", user_list, name="messages"),
    path('update-bio/', update_bio_view, name='update_bio'),
    path('create_post/', create_post, name='create_post'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('api/get_chat_messages/', views.get_messages, name='get_chat_messages'),
    path('profile/update_picture/', views.update_profile_picture, name='update_profile_picture'),
]