from django.urls import path
from .views import getAllCourses, getAllSchedules

urlpatterns = [
    path('all/',  getAllCourses, name="courses-all"),
    path('batches/<str:course_id>/',  getAllSchedules, name="schedules-all"),
]