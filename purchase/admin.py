from django.contrib import admin

from .models import Purchase
# Register your models here.


# class PurchaseModelAdmin(admin.ModelAdmin):
#     list_display = ['dummy']  # Specify the fields to display in the list view
#     search_fields = ['question', 'answer']  # Enable searching by specified fields
#     list_filter = ['question', 'faq_for']  # Enable filtering by specified fields
admin.site.register(Purchase)
