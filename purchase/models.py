from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User, Kid
from course.models import Course, Plans, Levels, Schedule
from simple_history.models import HistoricalRecords
# Create your models here.

class Purchase(models.Model):
    is_active = models.BooleanField(default=True, null=False, blank=False)
    user           = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Purchased By"), related_name='my_purchase')
    course_level   = models.ForeignKey(to=Levels, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Course Level Selected"))
    schedule       = models.ForeignKey(to=Schedule, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Batch Enrolled in"))
    plan_selected  = models.ForeignKey(to=Plans, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Plan Selected"))
    kids_selected  = models.ManyToManyField(to=Kid, related_name='my_purchases', blank=True)
    purchase_price = models.DecimalField(_("Price (Purchased With )"), max_digits=10, decimal_places=2)
    PAYMENT_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    )
    payment_status  = models.CharField(_("Payment Status"),max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    SESSION_STATUS_CHOICES = (
        ('Free Purchase', 'Free Purchase'),
        ('Razorpay', 'Razorpay'),
        ('Cashfree', 'Cashfree'),
    )
    payment_method  = models.CharField(_("Payment Method"),max_length=50, choices=SESSION_STATUS_CHOICES, null=True, blank=True)
    order_id        = models.CharField(_("Order ID"), max_length=200, null=True, blank=True)   
    payment_id      = models.CharField(_("Payment ID"), max_length=200, null=True, blank=True)   
    booking_id      = models.CharField(_("Booking ID"), max_length=120)
    order_signature = models.CharField(_("Razorpay Signature"), max_length=200, null=True, blank=True)   
    purchased_at    = models.DateTimeField(verbose_name="Purchased At", auto_now_add=True)
    last_modified_at= models.DateTimeField(verbose_name="Last Modified At", auto_now=True)
    history           = HistoricalRecords()

    class Meta:
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'

    def __str__(self) -> str:
        return f"{self.id} | {self.user}"


class PurchaseSession(models.Model):
    identifier       = models.CharField(max_length=100, unique=True)
    user             = models.ForeignKey(to=User, on_delete=models.CASCADE)                        
    course_selected  = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    plan_selected    = models.ForeignKey(to=Plans, on_delete=models.CASCADE)
    level_selected   = models.ForeignKey(to=Levels, on_delete=models.CASCADE)
    SESSION_STATUS_CHOICES = (
        ('INCOMPLETE', 'INCOMPLETE'),
        ('COMPLETED', 'COMPLETED'),
    )
    session_status   = models.CharField(max_length=20, choices=SESSION_STATUS_CHOICES, null=True, blank=True, default="INCOMPLETE", help_text="'COMPLETED' refers that user made purchase with this session. Purchase may be failed or succeeded.")

    class Meta:
        verbose_name = 'Purchase Session'
        verbose_name_plural = 'Purchase Sessions'
    
    def __str__(self) -> str:
        return f"{self.id} | {self.user}"