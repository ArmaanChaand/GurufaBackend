from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import  ValidationError
from course.models import Course
from user.models import User
from simple_history.models import HistoricalRecords
# Create your models here.
class FAQs(models.Model):
    FAQ_FOR_CHOICES = (
        ('GURUFA', 'GURUFA'),
        ('COURSE', 'COURSE'),
    )
    faq_for = models.CharField(_("FAQ is for?"), max_length=100, null=True, blank=True, choices=FAQ_FOR_CHOICES, help_text=_("Leave blank, if course is not chosen."))
    is_active  = models.BooleanField(default=False, null=False, blank=False)
    question   = models.CharField(_("Question"), max_length=200, blank=False, null=False)
    answer     = models.TextField(_("Answer"), blank=False, null=False)
    to_course    = models.ForeignKey(to=Course, 
                                blank=True,null=True, 
                                on_delete=models.SET_NULL, verbose_name=_("Course"),
                                related_name="course_faqs",
                                help_text=_("Leave blank, if FAQ is not for any Course.")
                                )
    
    history    = HistoricalRecords()

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self) -> str:
        course_selected = self.to_course or "GURUFA"
        return f"{self.question[:20]}... | [{course_selected}]"
    
    def save(self, *args, **kwargs):
        """Update faq_for accordingly"""
        if self.to_course:
            self.faq_for = 'COURSE'
        else:
            self.faq_for = 'GURUFA'
        super(FAQs, self).save(*args, **kwargs)

def validate_rating(value):
    if value > 5:
        raise ValidationError(_("Pick between 1 and 5"))

class Review(models.Model):
    REVIEW_FOR_CHOICES = (
        ('GURUFA', 'GURUFA'),
        ('COURSE', 'COURSE'),
    )
    review_for = models.CharField(_("Review is for?"), max_length=100, null=True, blank=True, choices=REVIEW_FOR_CHOICES, help_text=_("Leave blank, if course is not chosen."))
    is_active  = models.BooleanField(default=False, null=False, blank=False)
    review_by  = models.ForeignKey(to=User, verbose_name=_("Review given by"), on_delete=models.SET_NULL, null=True, blank=True, related_name='my_reviews')
    to_course  = models.ForeignKey(to=Course, verbose_name=_("Course"), on_delete=models.SET_NULL, null=True, blank=True, related_name='course_reviews', help_text=_("Leave blank, if Review is not for any Course."))
    rating     = models.DecimalField(max_digits=1, decimal_places=0, null=False, blank=False, validators=[validate_rating], help_text=_("Pick between 1 to 5"))
    content    = models.TextField(verbose_name=_("Content"), max_length=200, null=False, blank=False, help_text=_("Wrap up the review in less than 200 characters."))
    created_at = models.DateTimeField(null=True, blank=True)

    history    = HistoricalRecords()

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

        # Add a unique constraint to ensure a user can only review a course once
        unique_together = ('review_by', 'to_course')

    def clean(self):
        # Validate uniqueness of the review for a specific course and user
        existing_reviews = Review.objects.filter(review_by=self.review_by, to_course=self.to_course)
        if self.pk:
            existing_reviews = existing_reviews.exclude(pk=self.pk)  # Exclude current instance if editing
        if existing_reviews.exists():
            raise ValidationError(_("You have already reviewed this course."))
    
    
    def save(self, *args, **kwargs):
        """Update review_for accordingly"""
        if self.to_course:
            self.review_for = 'COURSE'
        else:
            self.review_for = 'GURUFA'
        super(Review, self).save(*args, **kwargs)
    

    def __str__(self) -> str:
        return f"{self.content[:30]}...]"


    