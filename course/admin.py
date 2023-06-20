from django.contrib import admin

# Register your models here.
from .models import Course
class CourseModelAdmin(admin.ModelAdmin):
    list_display = ['name']  # Specify the fields to display in the list view
    search_fields = ['name', 'overview', "about_guru"]  # Enable searching by specified fields

    fieldsets = [
        ('Course Description', {'fields': ['name', 'overview']}),
        ('Gurus', {'fields': ['about_guru']}),
    ]


admin.site.register(Course, CourseModelAdmin)