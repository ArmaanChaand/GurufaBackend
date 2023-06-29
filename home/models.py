from django.db import models
from django.utils.translation import gettext_lazy as _
from course.models import Course

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

    