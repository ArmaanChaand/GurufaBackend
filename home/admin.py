from django.contrib import admin

from .models import FAQs, Review
# Register your models here.

class FAQModelAdmin(admin.ModelAdmin):
    list_display = ['question', 'faq_for']  # Specify the fields to display in the list view
    search_fields = ['question', 'answer']  # Enable searching by specified fields
    list_filter = ['question', 'faq_for']  # Enable filtering by specified fields

admin.site.register(FAQs, FAQModelAdmin)


class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ['rating', 'to_course', 'review_by']  # Specify the fields to display in the list view
    list_filter = ['rating', 'to_course']  # Enable filtering by specified fields

    fieldsets = [
        ('Rating & Content', {'fields': ['rating', 'content']}),
        ('More', {'fields': ['review_by', 'to_course']}),
    ]

admin.site.register(Review, ReviewModelAdmin)