from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class CustomUserManager(BaseUserManager):
    
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
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
    first_name        = models.CharField(_("First name"), max_length=150, blank=False, null=False)
    last_name         = models.CharField(_("Last name"), max_length=150, blank=False, null=False)
    email             = models.EmailField(_("Email address"), blank=False, null=False, unique=True)
    is_email_verified = models.BooleanField(_("Email verified"), default=False, null=False, blank=False)
    phone_number      = PhoneNumberField(_("Phone Number "), blank=False, null=False)
    is_phone_verified = models.BooleanField(_("Phone verified"),default=False, null=False, blank=False)
    whatsapp_update   = models.BooleanField(_("Opted for WhatsApp Update"),default=False, null=False, blank=False)


    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
