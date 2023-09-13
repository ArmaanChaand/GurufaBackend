from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from .models import User, Kid, OTP
from guru.models import Guru
# Register your models here.
"""Associated Guru Model"""

class GuruModelInline(admin.TabularInline):
    model = Guru
    extra = 0

class KidModelInline(admin.TabularInline):
    model = Kid
    extra = 0

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'  # Include all fields, including 'password'

    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        required=False,  # Set as optional to avoid password validation on saving
    )
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'  # Include all fields, including 'password'

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
    )


# class UserModelAdmin(admin.ModelAdmin):
class UserModelAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'phone_number', 'user_roles']  # Specify the fields to display in the list view
    search_fields = ['email', 'phone_number', 'first_name', 'last_name']  # Enable searching by specified fields
    list_filter = ['auth_providers', 'is_a_guru','is_email_verified', 'is_phone_verified', 'date_joined', 'last_login']  # Enable filtering by specified fields

    fieldsets = [
        ('Auth Providers', {'fields': ['auth_providers']}),
        ('Guru Status', {'fields': ['user_roles', 'is_a_guru']}),
        ('Name and Picture', {'fields': ['first_name', 'last_name','picture', 'auth_provider_img', 'username']}),
        ('Email', {'fields': ['email', 'is_email_verified']}),
        ('Phone', {'fields': ['phone_number', 'is_phone_verified', 'whatsapp_update']}),
        ('Activity & Role', {'fields': ['is_active', 'is_staff', 'is_superuser']}),
        ('Date Joined & Last Login', {'fields': ['date_joined','last_login']}),
        ('Password', {'fields': ['password']}),  # Include password field here
    ]
    
    inlines = [KidModelInline, GuruModelInline]

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    def save_model(self, request, obj, form, change):
        # Manually hash the password if it has been changed
        if 'password' in form.changed_data:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)


admin.site.register(User, UserModelAdmin)

# Register Kid

class KidModelAdmin(admin.ModelAdmin):
    list_display = ['kid_first_name', 'kid_age', 'kid_parent'] 
    search_fields = ['kid_first_name', 'kid_last_name', 'kid_age']  
    list_filter = ['kid_age', 'kid_parent', 'is_active']  # Enable filtering by specified fields

    fieldsets = [
        ('Name', {'fields': ['kid_first_name', 'kid_last_name']}),
        ('Age', {'fields': ['kid_age']}),
        ('Gender', {'fields': ['kid_gender']}),
        ('Parent', {'fields': ['kid_parent']}), 
        ('Demo Courses', {'fields': ['demo_courses']}),  
        ('Activity Status', {'fields': ['is_active']}),  
    ]
admin.site.register(Kid, KidModelAdmin)
admin.site.register(OTP)