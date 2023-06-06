from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Course(models.Model):
    name     = models.CharField(_("Course Name"), max_length=200, null=False, blank=False)
    overview = models.TextField(_("Course Overview"), null=True, blank=True)