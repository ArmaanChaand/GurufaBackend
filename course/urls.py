from django.urls import path
from .views import getAllCourses, getAllBatches

urlpatterns = [
    path('all/',  getAllCourses, name="courses-all"),
    path('batches/',  getAllBatches, name="batches-all"),
]