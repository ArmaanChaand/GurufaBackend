from django.contrib import admin
from .models import Guru, BecomeAGuru

# Register your models here.
class GuruModelAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'get_phone_number']
    list_filter = ['experience', 'is_active']

    fieldsets = [
        ('User associated with', {'fields': ['user_id']}),
        ('More Info', {'fields': ['experience', 'guru_description']}),
        ('Activity Status', {'fields': ['is_active']}),
    ]
    def get_phone_number(self, obj):
        return obj.user_id.phone_number

    get_phone_number.short_description = 'Phone Number'


admin.site.register(Guru, GuruModelAdmin)


"""Become A Guru Form"""
admin.site.register(BecomeAGuru)