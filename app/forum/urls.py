from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('posts/', views.posts_view, name='posts'),
    path('profile/', views.profile_view, name='profile'),
    path("messages/", views.chat_list, name="messages"),
    path("chats/<int:chat_id>/", views.chat_detail, name="chat_detail"),
    path("chats/new/", views.create_chat_view, name="create_chat"),
    path("chats/<int:chat_id>/send/", views.send_message, name="send_message"),
    path("users/", views.user_list, name="user_list"),
    path("chats/", views.chat_list, name="chat_list"),
    path("messages/", views.user_list, name="messages"),
    path('update-bio/', views.update_bio_view, name='update_bio'),
    path('create_post/', views.create_post, name='create_post'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('api/get_chat_messages/', views.get_messages, name='get_chat_messages'),
    path('profile/update_picture/', views.update_profile_picture, name='update_profile_picture'),
    path('test-upload/', views.test_upload, name='test_upload'),
    path('tips/', views.tips_view, name='tips'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path("chats/new/<int:user_id>/", views.get_or_create_chat, name="get_or_create_chat"),
]