from django.db import models
from user.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_delete
from django.dispatch import receiver
# Create your models here.

class Guru(models.Model):
    user_id = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    experience = models.FloatField(_("Years Of Experience"), null=False, blank=False, default=0)

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