from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import  ValidationError
from course.models import Course
from user.models import User
# Create your models here.
class FAQs(models.Model):
    question = models.CharField(_("Question"), max_length=200, blank=False, null=False)
    answer = models.TextField(_("Answer"), blank=False, null=False)
    faq_for = models.ForeignKey(to=Course, 
                                blank=True,null=True, 
                                on_delete=models.SET_NULL, verbose_name=_("FAQ For"),
                                related_name="course_faqs",
                                )

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self) -> str:
        course_selected = self.faq_for or "GENERAL"
        return f"{self.question[:100]}... | [{course_selected}]"

def validate_rating(value):
    if value > 5:
        raise ValidationError(_("Pick between 1 and 5"))

class Review(models.Model):
    review_by = models.ForeignKey(to=User, verbose_name=_("Review given by"), on_delete=models.SET_NULL, null=True, blank=True, related_name='my_reviews')
    to_course = models.ForeignKey(to=Course, verbose_name=_("Course"), on_delete=models.SET_NULL, null=True, blank=True, related_name='course_reviews')
    rating    = models.DecimalField(max_digits=1, decimal_places=0, null=False, blank=False, default=1, validators=[validate_rating], help_text=_("Pick between 1 to 5"))
    content   = models.TextField(verbose_name=_("Content"), max_length=150, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self) -> str:
        return f"{self.content[:30]}...]"


    