from django.contrib import admin
from django import forms
from .models import Purchase, PurchaseSession
from user.models import Kid
from django.core.exceptions import ValidationError
# Register your models here.


# class PurchaseModelAdmin(admin.ModelAdmin):
#     list_display = ['dummy']  # Specify the fields to display in the list view
#     search_fields = ['question', 'answer']  # Enable searching by specified fields
#     list_filter = ['question', 'faq_for']  # Enable filtering by specified fields

class PurchaseAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['kids_selected'].queryset = self.instance.user.my_kids.all()
    
    def clean(self):
        cleaned_data = super().clean()
        selected_kids = cleaned_data.get('kids_selected')
        user = cleaned_data.get('user')
        
        if user and selected_kids.exists() and not selected_kids.filter(kid_parent=user).count() == selected_kids.count():
            raise ValidationError("Invalid selection: Kids must be related to the selected user.")
        
        return cleaned_data

class PurchaseAdmin(admin.ModelAdmin):
    form = PurchaseAdminForm

admin.site.register(Purchase, PurchaseAdmin )

class PurchaseSessionModelAdmin(admin.ModelAdmin):
    list_display = ['identifier', 'user', 'session_status'] 
    # search_fields = []  
    list_filter = ['session_status'] 

admin.site.register(PurchaseSession, PurchaseSessionModelAdmin)
