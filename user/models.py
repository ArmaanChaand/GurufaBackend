import uuid
from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from enum import Enum
from .validators import validate_kids_age
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from course.models import Course
# Create your models here.

class AuthProviders(Enum):
    AUTH_PROVIDER_EMAIL = 'Email'
    AUTH_PROVIDER_GOOGLE = 'Google'

class UserRoles(Enum):
    PARENT = 'Parent'
    GURU   = 'Guru'

import random

def generate_8_digit_random_number():
    # Generate a random number between 10000000 and 99999999 (inclusive)
    return random.randint(10000000, 99999999)

class CustomUserManager(BaseUserManager):
    
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        email = self.normalize_email(email)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email=email, password=password, **extra_fields)

class User(AbstractUser, PermissionsMixin): 
    picture           = models.ImageField(upload_to='images/users/', null=True, blank=True)
    auth_provider_img = models.URLField(null=True, blank=True)
    username          = models.CharField(_("Username"), max_length=100, null=True, blank=True)
    auth_providers    = models.CharField(_("Auth Providers"), max_length=100,null=False, blank=False,default='Email', choices=[(provider.value, provider.name) for provider in AuthProviders])
    user_roles        = models.CharField(_("User Role"), max_length=100,null=False, blank=False,default='Parent', choices=[(role.value, role.name) for role in UserRoles])
    is_a_guru         = models.BooleanField(_("Is A Guru?"), null=False, blank=False, default=False)
    first_name        = models.CharField(_("First name"), max_length=150, blank=False, null=False)
    last_name         = models.CharField(_("Last name"), max_length=150, blank=False, null=False)
    email             = models.EmailField(_("Email address"), blank=False, null=False, unique=True)
    is_email_verified = models.BooleanField(_("Email verified"), default=False, null=False, blank=False)
    phone_number      = PhoneNumberField(_("Phone Number "), blank=True, null=True, unique=True)
    is_phone_verified = models.BooleanField(_("Phone verified"),default=False, null=False, blank=False)
    whatsapp_update   = models.BooleanField(_("Opted for WhatsApp Update"),default=False, null=False, blank=False)

    history           = HistoricalRecords()
    
    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number"]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        """
           Add unique username to each users
        """
        if not self.username:
            random_string = str(uuid.uuid4().hex[:8])
            self.username = f"{self.first_name.lower()}{self.last_name.lower()}{random_string}"

        super().save(*args, **kwargs)
    
    @property
    def reviewed_courses_list(self):
        reviews = self.my_reviews.filter(is_active=True)
        reviewed_courses = [review.to_course.slug for review in reviews if review.to_course.is_active]
        return reviewed_courses

    @property
    def purchased_courses_list(self):
        purchases = self.my_purchase.filter(is_active=True, payment_status='PAID')
        purchased_courses = [purchase.course_level.to_course.slug for purchase in purchases]
        return purchased_courses

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    history    = HistoricalRecords()

    def __str__(self):
        return f"{self.user.username} - {self.otp_code}"
        
class KidsGender(Enum):
    MALE   = 'Male'
    FEMALE = 'Female'
    PNAS   = 'Prefer Not to Answer/State'



class Kid(models.Model):
    kid_parent        = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="my_kids")
    kid_profile       = models.ImageField(upload_to='images/kids/', null=True, blank=True, default='images/kids/kids_avatar.png', verbose_name=_("Kid's Profile Picture"))
    kid_gender        = models.CharField(_("Kid's Gender"), max_length=100,null=False, blank=False,default='Prefer Not to Answer/State', choices=[(gender.value, gender.name) for gender in KidsGender])
    kid_first_name    = models.CharField(_("First name"), max_length=50, blank=False, null=False)
    kid_last_name     = models.CharField(_("Last name"), max_length=50, blank=False, null=False)
    kid_age           = models.PositiveIntegerField(_("Kid's Age (In Years)"), default=5, validators=[validate_kids_age])
    is_active         = models.BooleanField(default=True, null=False, blank=False)
    demo_courses      = models.ManyToManyField(to=Course, related_name='kids_taken_demo', verbose_name="Demo Course Purchased", blank=True)

    history           = HistoricalRecords()


    class Meta:
        verbose_name = 'Kid'
        verbose_name_plural = 'Kids'
    
    def get_full_name(self):
        return  self.kid_first_name + " " + self.kid_last_name

    def __str__(self) -> str:
        return f"{self.get_full_name()} ({self.kid_parent})" 
    
    def clean(self) -> None:
        """Validate Number of Kids"""
        user = self.kid_parent
        if user and user.my_kids.filter(is_active=True).count() >= 7:
            raise ValidationError("A user can have a maximum of 7 kids.")
        return super().clean()
    
    def save(self, *args, **kwargs):
        """ Validate Name """
        self.kid_first_name = self.kid_first_name.capitalize()
        self.kid_last_name = self.kid_last_name.capitalize()
        super(Kid, self).save(*args, **kwargs)
    
"""

"""