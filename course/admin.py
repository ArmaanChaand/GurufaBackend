from django.contrib import admin

# Register your models here.
from .models import Course, Levels, Plans, Schedule, ScheduleTiming
from home.models import FAQs, Review

class LevelsModelInline(admin.TabularInline):
    model = Levels
    extra = 0

class FAQsModelInline(admin.TabularInline):
    model = FAQs
    extra = 0
    
class ScheduleModelInline(admin.TabularInline):
    model = Schedule
    extra = 0

class ReviewModelInline(admin.TabularInline):
    model = Review
    extra = 0

class CourseModelAdmin(admin.ModelAdmin):
    list_display = ['name']  # Specify the fields to display in the list view
    search_fields = ['name', 'overview', "about_guru"]  # Enable searching by specified fields

    fieldsets = [
        ('Course Description', {'fields': ['name', 'overview']}),
        ('Course Images', {'fields': ['course_icon', 'course_banner']}),
        ('Gurus', {'fields': ['about_guru']}),
    ]

    inlines = [LevelsModelInline, ScheduleModelInline, FAQsModelInline, ReviewModelInline]
    
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
        ('Plan Prices', {'fields': ['price', 'discount_percent']}),
    ]
admin.site.register(Plans, PlansModelAdmin)

class ScheduleTimingModelInline(admin.TabularInline):
    model = ScheduleTiming
    extra = 0

class ScheduleModelAdmin(admin.ModelAdmin):
    list_display = ['schedule_name', 'start_date', 'end_date']
    fieldsets = [
        ('Schedule Name', {'fields': ['schedule_name']}),
        ('Schedule for Course', {'fields': ['to_course']}),
        ('Schedule for Guru', {'fields': ['guru']}),
        ('Plan Associated', {'fields': ['plan']}),
        ('Start and End date', {'fields': ['start_date', 'end_date']}),
        ('Number of Seats', {'fields': ['total_num_of_seats', 'seats_occupied']}),
    ]
    inlines = [ScheduleTimingModelInline]
admin.site.register(Schedule, ScheduleModelAdmin)

class ScheduleTimingModelAdmin(admin.ModelAdmin):
    list_display = ['day', 'start_time', 'batch']
    fieldsets = [
        ('Day', {'fields': ['day']}),
        ('Batch Timing', {'fields': ['start_time', 'end_time']}),
    ]

admin.site.register(ScheduleTiming, ScheduleTimingModelAdmin)


