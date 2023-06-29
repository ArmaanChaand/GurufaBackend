from django.contrib import admin

# Register your models here.
from .models import Course, Levels, Plans, Batch, BatchTiming
from home.models import FAQs

class LevelsModelInline(admin.TabularInline):
    model = Levels
    extra = 0

class FAQsModelInline(admin.TabularInline):
    model = FAQs
    extra = 0

class CourseModelAdmin(admin.ModelAdmin):
    list_display = ['name']  # Specify the fields to display in the list view
    search_fields = ['name', 'overview', "about_guru"]  # Enable searching by specified fields

    fieldsets = [
        ('Course Description', {'fields': ['name', 'overview']}),
        ('Course Images', {'fields': ['course_icon', 'course_banner']}),
        ('Gurus', {'fields': ['about_guru']}),
    ]

    inlines = [LevelsModelInline, FAQsModelInline]
    
admin.site.register(Course, CourseModelAdmin)


class LevelsModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'to_course']  # Specify the fields to display in the list view
    list_filter = ['name', 'to_course']
    fieldsets = [
        ('Level Description', {'fields': ['name', 'description', 'to_course']}),
        ('Level Details', {'fields': ['num_classes', 'frequency', 'duration']}),
    ]
admin.site.register(Levels, LevelsModelAdmin)

class PlansModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Plan Description', {'fields': ['name', 'description']}),
        ('Siblings', {'fields': ['count_sibling']}),
        ('Plan Prices', {'fields': ['actual_price', 'original_price']}),
    ]
admin.site.register(Plans, PlansModelAdmin)

class BatchTimingModelInline(admin.TabularInline):
    model = BatchTiming
    extra = 0

class BatchModelAdmin(admin.ModelAdmin):
    list_display = ['batch_name', 'start_date', 'end_date']
    fieldsets = [
        ('Batch Name', {'fields': ['batch_name']}),
        ('Start and End date', {'fields': ['start_date', 'end_date']}),
        ('Number of Seats', {'fields': ['total_num_of_seats', 'seats_occupied']}),
    ]
    inlines = [BatchTimingModelInline]
admin.site.register(Batch, BatchModelAdmin)

class BatchTimingModelAdmin(admin.ModelAdmin):
    list_display = ['day', 'start_time', 'batch']
    fieldsets = [
        ('Day', {'fields': ['day']}),
        ('Batch Timing', {'fields': ['start_time', 'end_time']}),
    ]

admin.site.register(BatchTiming, BatchTimingModelAdmin)


