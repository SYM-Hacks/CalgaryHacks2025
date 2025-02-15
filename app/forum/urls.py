from django.urls import path
from .views import home  # Ensure this is correctly imported

urlpatterns = [
    path('', home, name='home'),  # Define at least one valid URL pattern
]
