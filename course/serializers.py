from rest_framework import serializers
from .models import Course, Levels, Plans, Schedule, Session
from home.serializers import FAQsSerializer
from datetime import date
from user.serializers import kidInfoSerializer
from guru.serializers import GuruSerializerForSchedule
from home.models import Review
from django.db import models

class PlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plans
        fields = ['id', 'name','slug', 'description', 'price', 'discounted_price', 'discount_percent']

class CourseSerializerSmall(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'course_icon', 'slug']

class LevelsSerializer(serializers.ModelSerializer):
    to_course = CourseSerializerSmall(many=False, read_only=True)
    class Meta:
        model = Levels
        fields = [
                    'id', 'name', 'description','increment', 'decrement', 
                    'num_classes', 'frequency', 'duration',
                    'to_course', 
                ]

class CourseSerializer(serializers.ModelSerializer):
    my_levels = LevelsSerializer(many=True, read_only=True)
    my_plans = PlansSerializer(many=True, read_only=True)
    course_faqs = FAQsSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'name','slug','title','overview','course_icon', 'course_banner', 'course_banner_url',
            'review_count', 'average_rating', 'purchase_count','participants_count',
            'max_capacity', 'min_num_classes', 'min_frequency', 'min_duration', 'starting_price',
            'my_plans', 'my_levels', 'course_faqs', 
        ]
    

class SessionSerializer(serializers.ModelSerializer):
    day = serializers.SerializerMethodField()
    class Meta:
        model = Session
        fields = ['id', 'date', 'start_time', 'end_time', 'day']
    
    def get_day(self, obj):
        return obj.date.strftime("%A")
    
    
class ScheduleSerializer(serializers.ModelSerializer):
    guru = GuruSerializerForSchedule(many=False, read_only=True)
    timings_by_day = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ('id', 'schedule_name', 'start_date', 'end_date', 'seats_left', 'to_course_level', 'guru', 'timings_by_day')

    def get_timings_by_day(self, obj):
        # Get all active timings related to this Schedule
        all_timings = obj.timing.filter(is_active=True).order_by('date', 'start_time').all()

        # Create a dictionary to store unique timings by day of the week
        unique_timings_by_day = {}

        for timing in all_timings:
            day = timing.date.strftime("%A")

            # Check if the day is already in the dictionary
            if day not in unique_timings_by_day:
                unique_timings_by_day[day] = SessionSerializer(timing).data

        # Arrange the timings by days of the week (Monday to Sunday)
        arranged_timings = []
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        for day in days_of_week:
            if day in unique_timings_by_day:
                arranged_timings.append(unique_timings_by_day[day])

        return arranged_timings




    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     current_date = date.today()
        
    #     if instance.end_date < current_date:
    #         """If end date has passed, return an empty representation"""
    #         representation = {}
        
    #     return representation   
