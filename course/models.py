import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords
# Create your models here.

def validate_course_icon_size(value):
    """Maximum allowed file size in bytes (200KB)"""
    max_size = 200 * 1024

    if value.size > max_size:
        raise ValidationError(_("The file size must be less than 200KB."))  

def validate_course_banner_size(value):
    """Maximum allowed file size in bytes (200KB)"""
    max_size = 800 * 1024

    if value.size > max_size:
        raise ValidationError(_("The file size must be less than 800KB."))  

class Course(models.Model):
    is_active = models.BooleanField(default=True, null=False, blank=False)
    name          = models.CharField(_("Course Name"), max_length=200, null=False, blank=False)
    slug          = models.SlugField(_("Slug"), max_length=200, unique=True, editable=False)
    overview      = models.TextField(_("Course Overview"), null=True, blank=True)
    about_guru    = models.TextField(_("About Guru"), null=True, blank=True)
    course_icon   = models.ImageField(upload_to='images/courses/', validators=[validate_course_icon_size])
    course_banner = models.ImageField(upload_to='images/courses/', validators=[validate_course_banner_size])

    history       = HistoricalRecords()

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
    
    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug or self.pk is None:
            self.slug = slugify(self.name) + str(uuid.uuid4().hex[:8])
        super().save(*args, **kwargs)
    
    def get_max_capacity(self):
        max_total_num_of_seats = self.course_schedules.aggregate(max_total_num_of_seats=models.Max('total_num_of_seats'))
        return max_total_num_of_seats['max_total_num_of_seats'] or 5
    

class Levels(models.Model):
    is_active = models.BooleanField(default=True, null=False, blank=False)
    to_course   = models.ForeignKey(to=Course, on_delete=models.CASCADE, null=False, blank=False, related_name='my_levels')
    name        = models.CharField(_("Level Name"), max_length=100, null=False, blank=False)
    description = models.CharField(_("Level Description"), max_length=100, null=False, blank=False, default='Every Grandmaster Was A Novice.')
    num_classes = models.IntegerField(_("Number Of Classes"), null=True, blank=True)
    frequency   = models.IntegerField(_("Frequency (days/week)"), null=True, blank=True)
    duration    = models.IntegerField(_("Duration of course (in weeks)"), null=True, blank=True)
    starts_from = models.DecimalField(_("Starts From"), max_digits=10, decimal_places=2)

    history     = HistoricalRecords()

    class Meta:
        verbose_name = 'Course Level'
        verbose_name_plural = 'Course Levels'
    
    def __str__(self) -> str:
        return f"{ self.name } ({self.to_course})"
    
class Plans(models.Model):
    PLAN_NAMES_CHOICES = (
        ('One-on-One', 'One-on-One'),
        ('Batch', 'Batch'),
        ('Siblings', 'Siblings'),
        ('Demo Class', 'Demo Class'),
    )
    name               = models.CharField(_("Plan Name"), max_length=100, null=False, blank=False, choices=PLAN_NAMES_CHOICES)
    slug               = models.SlugField(_("Slug"), max_length=200, unique=True, editable=False)
    description        = models.CharField(_("Plan Description"), max_length=100, null=True, blank=True)
    price              = models.DecimalField(_("Price"), max_digits=10, decimal_places=2,)
    discount_percent   = models.DecimalField(verbose_name=_("Discont per cent"),max_digits=5, decimal_places=2)
    is_active          = models.BooleanField(default=True, null=False, blank=False)

    history            = HistoricalRecords()

    @property
    def discounted_price(self):
        discount_amount = self.price * (self.discount_percent / 100)
        discounted_price = self.price - discount_amount
        return discounted_price

    class Meta:
        verbose_name = 'Course Plans'
        verbose_name_plural = 'Course Plans'
    
    def __str__(self) -> str:
        return f"{ self.name }" 
    
    def clean(self):
        discounted_price = self.discounted_price
        if discounted_price < 1:
            raise ValidationError("Discounted price cannot be less than 1. Modify Price and/or Discount per cent.")

    def save(self, *args, **kwargs):
        if not self.slug or self.pk is None:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Schedule(models.Model):
    is_active           = models.BooleanField(default=True, null=False, blank=False)
    to_course           = models.ForeignKey(to=Course, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Course"), related_name='course_schedules')
    plan                = models.ForeignKey(to=Plans, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Plan"))
    guru                = models.ForeignKey(to='guru.Guru', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Guru"),
                                           )
    schedule_name       = models.CharField(_("Schedule Name"), max_length=100)
    # start_date          = models.DateField(_("Start Date"))
    # end_date            = models.DateField(_("End Date"))
    total_num_of_seats  = models.DecimalField(_("Total Number of seats"),max_digits=3, decimal_places=0)
    seats_occupied      = models.DecimalField(_("Number of seats occupied"),max_digits=3, decimal_places=0)

    history             = HistoricalRecords()


    class Meta:
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules' 

    def __str__(self) -> str:
        return f"{self.schedule_name } | ({self.to_course})"

    @property
    def seats_left(self):
        return self.total_num_of_seats - self.seats_occupied

class ScheduleTiming(models.Model):
    is_active   = models.BooleanField(default=True, null=False, blank=False)
    batch       = models.ForeignKey(to=Schedule, on_delete=models.CASCADE, related_name='timing')
    date        = models.DateField(_("Date"))
    start_time  = models.TimeField(_("Start Time") )
    end_time    = models.TimeField(_("End Time ") )

    history     = HistoricalRecords()

    class Meta:
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions' 

    