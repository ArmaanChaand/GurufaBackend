from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError

from enum import Enum

# Create your models here.

class AuthProviders(Enum):
    AUTH_PROVIDER_EMAIL = 'Email'
    AUTH_PROVIDER_GOOGLE = 'Google'

class UserRoles(Enum):
    PARENT = 'Parent'
    GURU   = 'Guru'


class CustomUserManager(BaseUserManager):
    
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

class User(AbstractUser, PermissionsMixin): 
    username          = None
    auth_providers    = models.CharField(_("Auth Providers"), max_length=100,null=False, blank=False,default='Email', choices=[(provider.value, provider.name) for provider in AuthProviders])
    user_roles        = models.CharField(_("User Role"), max_length=100,null=False, blank=False,default='Parent', choices=[(role.value, role.name) for role in UserRoles])
    is_a_guru         = models.BooleanField(_("Is A Guru?"), null=False, blank=False, default=False)
    first_name        = models.CharField(_("First name"), max_length=150, blank=False, null=False)
    last_name         = models.CharField(_("Last name"), max_length=150, blank=False, null=False)
    email             = models.EmailField(_("Email address"), blank=False, null=False, unique=True)
    is_email_verified = models.BooleanField(_("Email verified"), default=False, null=False, blank=False)
    phone_number      = PhoneNumberField(_("Phone Number "), blank=False, null=False, unique=True,
                                            error_messages={
                                                "unique": _("Phone number already being used."),
                                            }
                                            )
    is_phone_verified = models.BooleanField(_("Phone verified"),default=False, null=False, blank=False)
    whatsapp_update   = models.BooleanField(_("Opted for WhatsApp Update"),default=False, null=False, blank=False)

    
    


    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number"]

    class Meta:
        verbose_name = 'User (Parent)'
        verbose_name_plural = 'Users (Parent)'
    
    def save(self, *args, **kwargs):
        """
            Raise validation error instead of Integrity Error
            in uniqueness of phone numbers
        """
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            raise ValidationError("Phone number already being used.")
        

class Kid(models.Model):
    kid_parent        = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="my_kids")
    kid_profile       = models.ImageField(upload_to='images/users/', null=True, blank=True)
    kid_first_name    = models.CharField(_("First name"), max_length=150, blank=False, null=False)
    kid_last_name     = models.CharField(_("Last name"), max_length=150, blank=False, null=False)
    kid_age           = models.PositiveIntegerField(_("Kid's Age (In Years)"), default=0)


    class Meta:
        verbose_name = 'Kid'
        verbose_name_plural = 'Kids'
    
    def get_full_name(self):
        return  self.kid_first_name + " " + self.kid_last_name

    def __str__(self) -> str:
        return f"{self.get_full_name()} ({self.kid_parent})" 
