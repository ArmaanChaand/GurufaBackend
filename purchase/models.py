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


    class Meta:
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'

    def __str__(self) -> str:
        return f"{self.id} | {self.user}"