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
    list_filter= ['is_active']

    fieldsets = [
        ('Course Description', {'fields': ['name', 'overview']}),
        ('Course Images', {'fields': ['course_icon', 'course_banner']}),
        ('Gurus', {'fields': ['about_guru']}),
        ('Activity Status', {'fields': ['is_active']}),
    ]

    inlines = [LevelsModelInline, ScheduleModelInline, FAQsModelInline, ReviewModelInline]
    
admin.site.register(Course, CourseModelAdmin)


class LevelsModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'to_course']  # Specify the fields to display in the list view
    list_filter = ['name', 'to_course', 'is_active']
    fieldsets = [
        ('Level Description', {'fields': ['name', 'description', 'to_course']}),
        ('Level Details', {'fields': ['num_classes', 'frequency', 'duration']}),
        ('Activity Status', {'fields': ['is_active']}),
    ]
admin.site.register(Levels, LevelsModelAdmin)

class PlansModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active']
    list_filter = ['is_active']
    fieldsets = [
        ('Plan Description', {'fields': ['name', 'description']}),
        ('Plan Prices', {'fields': ['price', 'discount_percent']}),
        ('Activity Status', {'fields': ['is_active']}),
    ]
admin.site.register(Plans, PlansModelAdmin)

class ScheduleTimingModelInline(admin.TabularInline):
    model = ScheduleTiming
    extra = 0

class ScheduleModelAdmin(admin.ModelAdmin):
    list_display = ['schedule_name', 'start_date', 'end_date', 'plan']
    list_filter = ['is_active']
    fieldsets = [
        ('Schedule Name', {'fields': ['schedule_name']}),
        ('Schedule for Course', {'fields': ['to_course']}),
        ('Schedule for Guru', {'fields': ['guru']}),
        ('Plan Associated', {'fields': ['plan']}),
        ('Start and End date', {'fields': ['start_date', 'end_date']}),
        ('Number of Seats', {'fields': ['total_num_of_seats', 'seats_occupied']}),
        ('Activity Status', {'fields': ['is_active']}),
    ]
    inlines = [ScheduleTimingModelInline]
admin.site.register(Schedule, ScheduleModelAdmin)

class ScheduleTimingModelAdmin(admin.ModelAdmin):
    list_display = ['date', 'start_time', 'batch']
    list_filter  = ['is_active', 'date']
    fieldsets = [
        ('Date', {'fields': ['date']}),
        ('Batch Timing', {'fields': ['start_time', 'end_time']}),
        ('Activity Status', {'fields': ['is_active']}),
    ]

admin.site.register(ScheduleTiming, ScheduleTimingModelAdmin)


