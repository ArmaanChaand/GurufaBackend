from datetime import datetime, time
from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User, Kid
from course.models import Course, Plans, Levels, Schedule
from simple_history.models import HistoricalRecords
# Create your models here.
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
        return f"{self.identifier} -•- {self.user}"

class Purchase(models.Model):
    is_active      = models.BooleanField(default=True, null=False, blank=False)
    user           = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Purchased By"), related_name='my_purchase')
    course_level   = models.ForeignKey(to=Levels, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Course Level Selected"), related_name='level_purchase')
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
    payment_platform  = models.CharField(_("Payment Method"),max_length=50, choices=SESSION_STATUS_CHOICES, null=True, blank=True)
    payment_method  = models.JSONField(_("Payment Method (JSON)"),null=True, blank=True)
    order_id        = models.CharField(_("Order ID"), max_length=200, null=True, blank=True)   
    payment_id      = models.CharField(_("Payment ID"), max_length=200, null=True, blank=True)   
    booking_id      = models.CharField(_("Booking ID"), max_length=120)
    order_signature = models.CharField(_("Razorpay Signature"), max_length=200, null=True, blank=True)   
    purchased_at    = models.DateTimeField(verbose_name="Purchased At", auto_now_add=True)
    last_modified_at= models.DateTimeField(verbose_name="Last Modified At", auto_now=True)
    purchase_session = models.ForeignKey(to=PurchaseSession, related_name='purchase', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Purchase Session")
    history           = HistoricalRecords()

    @property 
    def total_sessions(self):
        total_schedules =  self.course_level.course_level_schedules.filter(is_active=True)
        total_sessions = 0
        for schedule in total_schedules:
            total_sessions += schedule.timing.filter(is_active=True).count()
        return self.course_level.num_classes or total_sessions
    
    @property
    def completed_sessions(self):
        now = datetime.now()
        total_schedules =  self.course_level.course_level_schedules.filter(is_active=True)
        total_sessions = 0
        for schedule in total_schedules:
            sessions = schedule.timing.filter(is_active=True)
            for session in sessions:
                session_time = datetime.combine(session.date, session.start_time)
                if now > session_time:
                    total_sessions += 1
                    
        return total_sessions

    class Meta:
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'

    def __str__(self) -> str:
        return f"{self.id} | {self.user}"
