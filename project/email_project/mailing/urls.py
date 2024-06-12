from django.urls import path
from .views import register_view, home

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_view, name='register'),
]
