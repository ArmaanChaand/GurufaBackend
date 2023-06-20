from django.db import models

# Create your models here.
class FAQs(models.Model):
    question = models.CharField(max_length=200, blank=False, null=False)
    answer = models.TextField(blank=False, null=False)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
    