from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Purchase(models.Model):
    dummy = models.JSONField(verbose_name=_("Dummy"))

    class Meta:
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'

    # def __str__(self) -> str:
    #     return