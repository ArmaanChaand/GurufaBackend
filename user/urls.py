from django.urls import path, include
from .views import (userAPIView, registerUser, authenticateUser, logoutUser, getUserInfo,
                    getMyKids,saveMyKid, deleteAKid, getPurchasedCourses, updateUserName, updateUserKey,
                    updatePhoneNuber
                    )
from .socialsViews import googleOAuth2
from .verifyViews import verify_phone
urlpatterns = [

    path('auth/register/', registerUser , name="user-register"),
    path('auth/login/', authenticateUser , name="user-login"),
    path('auth/logout/', logoutUser , name="user-logout"),
    path('auth/google/', googleOAuth2 , name="user-google"),
    path('auth/verify/phone/', verify_phone , name="user-verify-otp"),

    path('edit/name/', updateUserName , name="user-edit-name"),
    path('edit/key/', updateUserKey , name="user-edit-key"),
    path('edit/phone/', updatePhoneNuber , name="user-edit-key"),
    
    path('info/', getUserInfo , name="user-info"),
    path('all/', userAPIView , name="user-all"),
    path('kid/all/', getMyKids , name="user-kid-all"),
    path('kid/new/', saveMyKid , name="user-kid-new"),
    path('kid/new/<int:kid_id>/', saveMyKid , name="user-kid-new"),
    path('kid/delete/<int:kid_id>/', deleteAKid , name="user-kid-delete"),
    path('purchase/all/', getPurchasedCourses , name="purchased-courses"),
    path('guru/', include('guru.urls'))
]