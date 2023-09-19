import os
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords
# Create your models here.

def validate_course_icon_file_type(value):
    # Get the file extension of the uploaded file
    ext = os.path.splitext(value.name)[1].lower()

    # List of allowed file extensions for images and SVG files
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']

    # Check if the file extension is in the list of allowed extensions
    if not ext in allowed_extensions:
        raise ValidationError("Only image files and SVG files are allowed.")

def validate_course_icon_size(value):
    """Maximum allowed file size in bytes (200KB)"""
    max_size = 200 * 1024

    if value.size > max_size:
        raise ValidationError(_("The file size must be less than 200KB."))  

def validate_course_banner_size(value):
    """Maximum allowed file size in bytes (5MB)"""
    max_size = 5 * 1024 * 1024

    if value.size > max_size:
        raise ValidationError(_("The file size must be less than 5MB."))  

class Course(models.Model):
    is_active = models.BooleanField(default=True, null=False, blank=False)
    name          = models.CharField(_("Course Name"), max_length=50, null=False, blank=False)
    title         = models.CharField(_("Course Title"), max_length=150, null=True, blank=True)
    slug          = models.SlugField(_("Slug"), max_length=200, unique=True, editable=True)
    overview      = models.TextField(_("Course Overview"), null=True, blank=True)
    course_icon   = models.FileField(upload_to='images/courses/', validators=[validate_course_icon_size, validate_course_icon_file_type], null=True, blank=True)
    course_banner = models.ImageField(upload_to='images/courses/', validators=[validate_course_banner_size], null=True, blank=True)
    course_banner_url = models.URLField(_("Course Banner URL"), null=True, blank=True)

    history       = HistoricalRecords()

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
    
    def __str__(self) -> str:
        return self.name
    
    def clean(self):
        # Validate that either 'course_banner' or 'course_banner_url' is provided, but not both.
        if self.course_banner and self.course_banner_url:
            raise ValidationError(_("You can only provide either a course banner image or a course banner URL, not both."))
        if not self.course_banner and not self.course_banner_url:
            raise ValidationError(_("You need to provide either a course banner image or a course banner URL."))
         # Check if the slug is unique.
        courses = Course.objects.exclude(id=self.id)
        for course in courses:
            if course.slug == self.slug:
                raise ValidationError(_("The slug must be unique."))

    

    def save(self, *args, **kwargs):
        # If a 'course_banner_url' is provided, set 'course_banner' to None to avoid conflicts.
        if self.course_banner_url:
            self.course_banner = None
        if not self.slug or self.pk is None:
            self.slug = slugify(self.name) + str(uuid.uuid4().hex[:8])
        super().save(*args, **kwargs)
    
    def get_max_capacity(self):
        schedules = self.course_schedules.filter(is_active=True)
        max_total_num_of_seats = schedules.aggregate(max_total_num_of_seats=models.Max('total_num_of_seats'))
        return max_total_num_of_seats['max_total_num_of_seats'] or 5
    

    def get_min_num_classes(self):
        schedules = self.course_schedules.filter(is_active=True)
        min_num_classes = schedules.aggregate(min_num_classes=models.Min('num_classes'))['min_num_classes']
        return min_num_classes or 0

    def get_min_frequency(self):
        schedules = self.course_schedules.filter(is_active=True)
        min_frequency = schedules.aggregate(min_frequency=models.Min('frequency'))['min_frequency']
        return min_frequency or 0

    def get_min_duration(self):
        schedules = self.course_schedules.filter(is_active=True)
        min_duration = schedules.aggregate(min_duration=models.Min('duration'))['min_duration']
        return min_duration or 0

    def get_starting_price(self):
        # Get all the plans linked with the course
        plans = self.my_plans.filter(is_active=True)

        # Initialize a list to store non-zero prices
        non_zero_prices = []

        # Check if there are any plans
        if plans:
            # Iterate through the plans and collect non-zero prices
            for plan in plans:
                if plan.price > 0:
                    non_zero_prices.append(plan.price)

            # If there are non-zero prices, find the minimum among them
            if non_zero_prices:
                min_non_zero_price = min(non_zero_prices)
                return min_non_zero_price
            else:
                # If all prices are zero, return zero or any other default value as needed
                return 0  # You can change this default value as needed
        else:
            # Return a default value if there are no plans
            return 0  # You can change this default value as needed
        
    

class Levels(models.Model):
    is_active = models.BooleanField(default=True, null=False, blank=False)
    to_course   = models.ForeignKey(to=Course, on_delete=models.CASCADE, null=False, blank=False, related_name='my_levels')
    name        = models.CharField(_("Level Name"), max_length=100, null=False, blank=False)
    description = models.CharField(_("Level Description"), max_length=100, null=False, blank=False, default='Every Grandmaster Was A Novice.')
    increment   = models.DecimalField(verbose_name=_("Increase price by: "), decimal_places=2, max_digits=50,default=0, null=True, blank=True)
    decrement   = models.DecimalField(verbose_name=_("Decrease price by: "), decimal_places=2, max_digits=50, default=0, null=True, blank=True)

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
        ('Group Sessions', 'Group Sessions'),
        ('Siblings', 'Siblings'),
        ('Demo Class', 'Demo Class'),
    )
    name               = models.CharField(_("Plan Name"), max_length=100, null=False, blank=False, choices=PLAN_NAMES_CHOICES)
    course             = models.ForeignKey(to=Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='my_plans')
    slug               = models.SlugField(_("Slug"), max_length=200, unique=True, editable=False)
    description        = models.CharField(_("Plan Description"), max_length=100, null=True, blank=True)
    price              = models.DecimalField(_("Price"), max_digits=10, decimal_places=2,)
    discount_percent   = models.DecimalField(verbose_name=_("Discont per cent"),max_digits=5, decimal_places=2, null=True, blank=True,default=0)
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
        return f"{ self.name } | { self.course }" 
    
    def clean(self):
        discounted_price = self.discounted_price
        if discounted_price < 1 and self.name != 'Demo Class':
            raise ValidationError("Discounted price cannot be less than 1. Modify Price and/or Discount per cent.")

    def save(self, *args, **kwargs):
        if not self.slug or self.pk is None:
            self.slug = slugify(self.name) + str(uuid.uuid4().hex[:8])
        super().save(*args, **kwargs)

class Schedule(models.Model):
    is_active           = models.BooleanField(default=True, null=False, blank=False)
    to_course           = models.ForeignKey(to=Course, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Course"), related_name='course_schedules')
    plan                = models.ForeignKey(to=Plans, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Plan"))
    guru                = models.ForeignKey(to='guru.Guru', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Guru"), related_name='plan_associated'
                                           )
    schedule_name       = models.CharField(_("Schedule Name"), max_length=100, null=True, blank=True, help_text='Leave blank to automaticallly assign a name.')
    total_num_of_seats  = models.DecimalField(_("Total Number of seats"),max_digits=3, decimal_places=0)
    seats_occupied      = models.DecimalField(_("Number of seats occupied"),max_digits=3, decimal_places=0)

    num_classes = models.IntegerField(_("Number Of Classes"), null=True, blank=True)
    frequency   = models.IntegerField(_("Frequency (days/week)"), null=True, blank=True)
    duration    = models.IntegerField(_("Duration of course (in weeks)"), null=True, blank=True)

    history             = HistoricalRecords()


    class Meta:
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules' 

    def __str__(self) -> str:
        return f"{self.schedule_name } | ({self.to_course})"
    
    def save(self, *args, **kwargs):
        schedule_name = f"Schedule | {self.to_course.name} | {self.plan.name}"
        try:
            first_session = self.timing.filter(is_active=True).first()
            if first_session:
                schedule_name += f" | {first_session.date}"
        except Exception as e:
            pass
        self.schedule_name = schedule_name
        super().save(*args, **kwargs)

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

    