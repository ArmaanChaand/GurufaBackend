from django.urls import path
from .api_views import userAPIView, registerUser, authenticateUser

urlpatterns = [
    path('', authenticateUser , name="user-info"),
    path('all/', userAPIView , name="user-all"),
    path('register/', registerUser , name="user-register"),
]