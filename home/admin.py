from django.contrib import admin

from .models import FAQs, Review
# Register your models here.

class FAQModelAdmin(admin.ModelAdmin):
    list_display = ['question', 'to_course', 'faq_for']  # Specify the fields to display in the list view
    list_filter = ['to_course', 'is_active', 'faq_for']  # Enable filtering by specified fields

    fieldsets = [
        ('Content', {'fields': ['question', 'answer']}),
        ('Course', {'fields': ['to_course']}),
        ('Activity Status', {'fields': ['is_active']}),
    ]

admin.site.register(FAQs, FAQModelAdmin)


class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ['rating', 'to_course', 'review_by', 'review_for']  # Specify the fields to display in the list view
    list_filter = ['rating', 'to_course', 'is_active', 'review_for']  # Enable filtering by specified fields

    fieldsets = [
        ('Rating & Content', {'fields': ['rating', 'content']}),
        ('More', {'fields': ['review_by', 'to_course', 'created_at']}),
        ('Activity Status', {'fields': ['is_active']}),
    ]

admin.site.register(Review, ReviewModelAdmin)