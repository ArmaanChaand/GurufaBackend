from django.contrib import admin

from .models import FAQs
# Register your models here.

class FAQModelAdmin(admin.ModelAdmin):
    list_display = ['question', 'faq_for']  # Specify the fields to display in the list view
    search_fields = ['question', 'answer']  # Enable searching by specified fields
    list_filter = ['question', 'faq_for']  # Enable filtering by specified fields




admin.site.register(FAQs, FAQModelAdmin)
