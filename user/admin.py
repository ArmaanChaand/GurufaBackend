from django.contrib import admin
from .models import User

# Register your models here.
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email', 'phone_number']  # Specify the fields to display in the list view
    search_fields = ['email', 'phone_number', 'first_name', 'last_name']  # Enable searching by specified fields
    list_filter = ['is_email_verified', 'is_phone_verified', 'date_joined', 'last_login']  # Enable filtering by specified fields

    fieldsets = [
        ('Name', {'fields': ['first_name', 'last_name']}),
        ('Email', {'fields': ['email', 'is_email_verified']}),
        ('Phone', {'fields': ['phone_number', 'is_phone_verified', 'whatsapp_update']}),
        ('password', {'fields': ['password']}),
        ('Activity & Role', {'fields': ['is_active', 'is_staff', 'is_superuser']}),
        ('Date Joined & Last Login', {'fields': ['date_joined','last_login']}),
    ]


admin.site.register(User, UserModelAdmin)