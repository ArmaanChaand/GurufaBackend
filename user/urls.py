from django.urls import path
from .api_views import userAPIView, registerUser

urlpatterns = [
    path('', userAPIView , name="user-home"),
    path('register/', registerUser , name="user-register"),
]