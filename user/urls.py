from django.urls import path, include
from .views import (userAPIView, registerUser, authenticateUser, logoutUser, getUserInfo,
                    getMyKids,saveMyKid, deleteAKid, getPurchasedCourses,
                    
                    )
from .socialsViews import googleOAuth2

urlpatterns = [

    path('auth/register/', registerUser , name="user-register"),
    path('auth/login/', authenticateUser , name="user-login"),
    path('auth/logout/', logoutUser , name="user-logout"),
    path('auth/google/', googleOAuth2 , name="user-google"),
    
    path('info/', getUserInfo , name="user-info"),
    path('all/', userAPIView , name="user-all"),
    path('kid/all/', getMyKids , name="user-kid-all"),
    path('kid/new/', saveMyKid , name="user-kid-new"),
    path('kid/new/<int:kid_id>/', saveMyKid , name="user-kid-new"),
    path('kid/delete/<int:kid_id>/', deleteAKid , name="user-kid-delete"),
    path('purchase/all/', getPurchasedCourses , name="purchased-courses"),
    path('guru/', include('guru.urls'))
]