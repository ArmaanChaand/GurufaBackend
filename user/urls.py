from django.urls import path
from .views import userAPIView, registerUser, authenticateUser, logoutUser, getUserInfo

urlpatterns = [
    path('register/', registerUser , name="user-register"),
    path('login/', authenticateUser , name="user-login"),
    path('logout/', logoutUser , name="user-logout"),
    path('info/', getUserInfo , name="user-info"),
    path('all/', userAPIView , name="user-all"),
]