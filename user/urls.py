from django.urls import path, include
from .views import (userAPIView, registerUser, authenticateUser, logoutUser, getUserInfo,
                    getMyKids,saveMyKid,
                    )

urlpatterns = [

    path('register/', registerUser , name="user-register"),
    path('login/', authenticateUser , name="user-login"),
    path('logout/', logoutUser , name="user-logout"),
    path('info/', getUserInfo , name="user-info"),
    path('all/', userAPIView , name="user-all"),
    path('kid/all/', getMyKids , name="user-kid-all"),
    path('kid/new/', saveMyKid , name="user-kid-new"),
    path('kid/new/<int:kid_id>/', saveMyKid , name="user-kid-new"),

    path('guru/', include('guru.urls'))
]