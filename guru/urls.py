from django.urls import path
from .views import becomeAGuruView, RetrieveBecomeAGuru

urlpatterns = [
    path('apply/', becomeAGuruView , name="apply-guru"),
    path('retrieve/<str:pk>/', RetrieveBecomeAGuru.as_view() , name="apply-guru"),
]