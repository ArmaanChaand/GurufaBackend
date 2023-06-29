from django.urls import path
from .views import CreatePurchase

urlpatterns = [
    path('create/',  CreatePurchase, name="create-purchase"),
]