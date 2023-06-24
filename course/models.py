from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

# Create your models here.
class Course(models.Model):
    name       = models.CharField(_("Course Name"), max_length=200, null=False, blank=False)
    slug       = models.SlugField(_("Slug"), max_length=200, unique=True, editable=False)
    overview   = models.TextField(_("Course Overview"), null=True, blank=True)
    about_guru = models.TextField(_("About Guru"), null=True, blank=True)
    
    # def save(self, *args, **kwargs):
    #     if not self.slug or self.pk is None:
    #         self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)
