from django.db import models
from user.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_delete
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField
from simple_history.models import HistoricalRecords
# Create your models here.

class Guru(models.Model):
    is_active        = models.BooleanField(default=True, null=False, blank=False)
    user_id          = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    guru_description = models.TextField(null=True, blank=True)
    experience       = models.FloatField(_("Years Of Experience"), null=False, blank=False, default=0)

    history     = HistoricalRecords()

    class Meta:
        verbose_name = 'Guru'
        verbose_name_plural = 'Gurus'
    
    def __str__(self) -> str:
        return self.user_id.get_full_name() + "(GURU)"
    
    def save(self, *args, **kwargs):
        """
            Update Guru Status of User model when a new instance of Guru is created
        """
        if not self.pk:  # If it's a new instance
            self.user_id.user_roles = 'Guru'
            self.user_id.is_a_guru = True
            self.user_id.save()

        super().save(*args, **kwargs)
    
@receiver(post_delete, sender=Guru)
def update_user_roles(sender, instance, **kwargs):
    instance.user_id.user_roles = 'Parent'
    instance.user_id.is_a_guru = False
    instance.user_id.save()


SKILLS_CHOICES = (
    ("Chess", "Chess"),
    ("Rubik's Cube", "Rubik's Cube"),
    ("Vedic Maths", "Vedic Maths"),
    ("Yoga", "Yoga"),
    ("Other", "Other"),
)
EXPERIENCE_CHOICES = (
    ("0 Years", "0 Years"),
    ("1-3 Years", "1-3 Years"),
    ("More Than 3 Years", "More Than 3 Years"),
)
class BecomeAGuru(models.Model):
    full_name         = models.CharField(_("Full name"), max_length=100, blank=False, null=False)
    email             = models.EmailField(_("Email address"), blank=False, null=False)
    phone_number      = PhoneNumberField(_("Phone Number "), blank=False, null=False)
    yrs_experience    = models.CharField(verbose_name=_("Years of teaching experience"),max_length=50, choices=EXPERIENCE_CHOICES, blank=False, null=False)
    skills            = MultiSelectField(max_length=100, max_choices=5, verbose_name=_("Skills"), choices=SKILLS_CHOICES, blank=False, null=False)
    other_skills      = models.CharField(_("Other Skills"), max_length=100, blank=True, null=True)

    history           = HistoricalRecords()
    
    class Meta:
        verbose_name = 'Become A Guru Application'
        verbose_name_plural = 'Become A Guru Applications'
    
    def __str__(self) -> str:
        return f"{self.full_name}" 