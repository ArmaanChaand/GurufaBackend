from django.urls import path
from .views import getAllCourses

urlpatterns = [
    path('all/',  getAllCourses, name="courses-all"),
]