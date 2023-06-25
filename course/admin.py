from django.contrib import admin

# Register your models here.
from .models import Course, Levels

class LevelsModelInline(admin.TabularInline):
    model = Levels
    extra = 0


class CourseModelAdmin(admin.ModelAdmin):
    list_display = ['name']  # Specify the fields to display in the list view
    search_fields = ['name', 'overview', "about_guru"]  # Enable searching by specified fields

    fieldsets = [
        ('Course Description', {'fields': ['name', 'overview']}),
        ('Gurus', {'fields': ['about_guru']}),
    ]

    inlines = [LevelsModelInline]

class LevelsModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'to_course']  # Specify the fields to display in the list view
    list_filter = ['name', 'to_course']

    fieldsets = [
        ('Name and Course', {'fields': ['name', 'to_course']}),
        ('Level Description', {'fields': ['num_classes', 'frequency', 'duration']}),
    ]


admin.site.register(Course, CourseModelAdmin)
admin.site.register(Levels, LevelsModelAdmin)