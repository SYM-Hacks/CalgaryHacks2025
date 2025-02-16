from django.urls import path
from .views import home, signup, login_view, logout_view, posts_view, messaging_view, get_messages, send_message

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('posts/', posts_view, name='posts'),
    path('messages/', messaging_view, name='messages'),
    path('messages/', messaging_view, name='messages'),
    path('api/get_messages/', get_messages, name='get_messages'),
    path('api/send_message/', send_message, name='send_message'),
]

