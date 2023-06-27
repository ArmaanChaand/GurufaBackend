from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

# Create your models here.
class Course(models.Model):
    name       = models.CharField(_("Course Name"), max_length=200, null=False, blank=False)
    slug       = models.SlugField(_("Slug"), max_length=200, unique=True, editable=False)
    overview   = models.TextField(_("Course Overview"), null=True, blank=True)
    about_guru = models.TextField(_("About Guru"), null=True, blank=True)
    
    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
    
    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug or self.pk is None:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    

class Levels(models.Model):
    to_course   = models.ForeignKey(to=Course, on_delete=models.CASCADE, null=False, blank=False, related_name='my_levels')
    name        = models.CharField(_("Level Name"), max_length=100, null=False, blank=False)
    description = models.CharField(_("Level Description"), max_length=100, null=False, blank=False, default='Every Grandmaster Was A Novice.')
    num_classes = models.IntegerField(_("Number Of Classes"), null=True, blank=True)
    frequency   = models.IntegerField(_("Frequency (days/week)"), null=True, blank=True)
    duration    = models.IntegerField(_("Duration of course (in weeks)"), null=True, blank=True)
    starts_from = models.DecimalField(_("Starts From"), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Course Level'
        verbose_name_plural = 'Course Levels'
    
    def __str__(self) -> str:
        return f"{ self.name } ({self.to_course})"
    
class Plans(models.Model):
    name        = models.CharField(_("Plan Name"), max_length=100, null=False, blank=False)
    description = models.CharField(_("Plan Description"), max_length=100, null=False, blank=False)
    actual_price = models.DecimalField(_("Price (Discounted)"), max_digits=10, decimal_places=2)
    original_price = models.DecimalField(_("Original Price"), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Course Plans'
        verbose_name_plural = 'Course Plans'
    
    def __str__(self) -> str:
        return f"{ self.name }"
    

    