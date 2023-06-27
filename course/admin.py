from django.contrib import admin

# Register your models here.
from .models import Course, Levels, Plans

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
        ('Level Description', {'fields': ['name', 'description', 'to_course']}),
        ('Level Details', {'fields': ['num_classes', 'frequency', 'duration']}),
    ]
class PlansModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Plan Description', {'fields': ['name', 'description']}),
        ('Plan Details', {'fields': ['actual_price', 'original_price']}),
    ]


admin.site.register(Course, CourseModelAdmin)
admin.site.register(Levels, LevelsModelAdmin)
admin.site.register(Plans, PlansModelAdmin)