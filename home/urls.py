from django.urls import path
from .views import getAllFaqs

urlpatterns = [
   path('faqs/', getAllFaqs, name='all-faqs')
]