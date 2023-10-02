from django.urls import path
from .views import getAllFaqs,getCourseFaqs, getAllReviews, getCourseReviews, createReview

urlpatterns = [
   path('faqs/', getAllFaqs, name='all-faqs'),
   path('faqs/<str:course_slug>/', getCourseFaqs, name='course-faqs'),
   path('reviews/', getAllReviews, name='all-reviws'),
   path('reviews/course/<int:course_id>/', getCourseReviews, name='course-reviews'),
   path('reviews/new/', createReview, name='create-review')
]