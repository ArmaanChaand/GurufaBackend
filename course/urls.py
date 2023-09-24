from django.urls import path
from .views import getAllCourses, getAllSchedules

urlpatterns = [
    path('all/',  getAllCourses, name="courses-all"),
    path('schedules/<str:course_level_id>/',  getAllSchedules, name="schedules-all"),
]