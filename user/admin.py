from django.contrib import admin
from .models import User, Kid
from guru.models import Guru
# Register your models here.
"""Associated Guru Model"""

class GuruModelInline(admin.TabularInline):
    model = Guru
    extra = 0

class KidModelInline(admin.TabularInline):
    model = Kid
    extra = 0


class UserModelAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email', 'phone_number', 'auth_providers']  # Specify the fields to display in the list view
    search_fields = ['email', 'phone_number', 'first_name', 'last_name']  # Enable searching by specified fields
    list_filter = ['auth_providers', 'is_a_guru','is_email_verified', 'is_phone_verified', 'date_joined', 'last_login']  # Enable filtering by specified fields

    fieldsets = [
        ('Auth Providers', {'fields': ['auth_providers']}),
        ('Guru Status', {'fields': ['user_roles', 'is_a_guru']}),
        ('Name and Picture', {'fields': ['first_name', 'last_name','picture', 'auth_provider_img', 'username']}),
        ('Email', {'fields': ['email', 'is_email_verified']}),
        ('Phone', {'fields': ['phone_number', 'is_phone_verified', 'whatsapp_update']}),
        ('password', {'fields': ['password']}),
        ('Activity & Role', {'fields': ['is_active', 'is_staff', 'is_superuser']}),
        ('Date Joined & Last Login', {'fields': ['date_joined','last_login']}),
    ]
    inlines = [KidModelInline, GuruModelInline]


admin.site.register(User, UserModelAdmin)

# Register Kid

class KidModelAdmin(admin.ModelAdmin):
    list_display = ['kid_first_name', 'kid_age', 'kid_parent'] 
    search_fields = ['kid_first_name', 'kid_last_name', 'kid_age']  
    list_filter = ['kid_age', 'kid_parent']  # Enable filtering by specified fields

    fieldsets = [
        ('Name', {'fields': ['kid_first_name', 'kid_last_name']}),
        ('Age', {'fields': ['kid_age']}),
        ('Parent', {'fields': ['kid_parent']}), 
    ]
admin.site.register(Kid, KidModelAdmin)