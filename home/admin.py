from django.contrib import admin

from .models import FAQs
# Register your models here.

class FAQModelAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer']  # Specify the fields to display in the list view
    search_fields = ['question', 'answer']  # Enable searching by specified fields
    list_filter = ['question', 'answer']  # Enable filtering by specified fields


admin.site.register(FAQs, FAQModelAdmin)
