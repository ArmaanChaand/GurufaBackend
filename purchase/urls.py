from django.urls import path
from .views import (CreatePurchase, successPurchaseRazorpay, failedPurchaseRazorpay, 
                    getOrderCashfree, CreatePurchaseSession, getPurchaseSession)

urlpatterns = [
    path('create/',  CreatePurchase, name="create-purchase"),
    path('session/create/',  CreatePurchaseSession, name="create-purchase-session"),
    path('session/retrieve/<str:identifier>/',  getPurchaseSession, name="get-purchase-session"),
    path('razorpay/successful/',  successPurchaseRazorpay, name="success-purchase-razorpay"),
    path('razorpay/failed/',  failedPurchaseRazorpay, name="failed-purchase-razorpay"),
    path('cashfree/getorder/',  getOrderCashfree, name="get-order-cashfree"),
]