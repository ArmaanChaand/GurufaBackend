from django.urls import path
from .views import CreatePurchase, successPurchaseRazorpay, failedPurchaseRazorpay

urlpatterns = [
    path('create/',  CreatePurchase, name="create-purchase"),
    path('razorpay/successful/',  successPurchaseRazorpay, name="success-purchase-razorpay"),
    path('razorpay/failed/',  failedPurchaseRazorpay, name="failed-purchase-razorpay"),
]