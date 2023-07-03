from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User, Kid
from course.models import Course, Plans, Levels, Schedule
# Create your models here.

class Purchase(models.Model):
    user           = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Purchased By"), related_name='my_purchase')
    course_level   = models.ForeignKey(to=Levels, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Course Level Selected"))
    schedule       = models.ForeignKey(to=Schedule, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Batch Enrolled in"))
    plan_selected  = models.ForeignKey(to=Plans, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Plan Selected"))
    kids_selected  = models.ManyToManyField(to=Kid, related_name='my_purchases', null=True, blank=True)
    purchase_price = models.DecimalField(_("Price (Purchased With )"), max_digits=10, decimal_places=2)
    PAYMENT_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    )
    payment_status  = models.CharField(_("Payment Status"),max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    order_id        = models.CharField(_("Order ID"), max_length=200, null=True, blank=True)   
    payment_id      = models.CharField(_("Payment ID"), max_length=200, null=True, blank=True)   
    order_signature = models.CharField(_("Razorpay Signature"), max_length=200, null=True, blank=True)   
     

    class Meta:
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'

    def __str__(self) -> str:
        return f"{self.id} | {self.user}"