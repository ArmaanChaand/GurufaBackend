from django.urls import path
from .api_views import userAPIView, registerUser, authenticateUser, logoutUser

urlpatterns = [
    path('login/', authenticateUser , name="user-login"),
    path('logout/', logoutUser , name="user-logout"),
    path('all/', userAPIView , name="user-all"),
    path('register/', registerUser , name="user-register"),
]