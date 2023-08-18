from rest_framework import serializers
from .models import Course, Levels, Plans, Schedule, ScheduleTiming
from home.serializers import FAQsSerializer
from datetime import date
from user.serializers import kidInfoSerializer

class PlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plans
        fields = ['id', 'name','slug', 'description', 'price', 'discounted_price', 'discount_percent']

class CourseSerializerSmall(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name','course_icon', 'slug']

class LevelsSerializer(serializers.ModelSerializer):
    to_course = CourseSerializerSmall(many=False, read_only=True)
    class Meta:
        model = Levels
        fields = ['id', 'name', 'description', 'num_classes', 'frequency', 'duration', 'starts_from', 'to_course']

class CourseSerializer(serializers.ModelSerializer):
    my_levels = LevelsSerializer(many=True, read_only=True)
    course_faqs = FAQsSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ['id', 'name','course_icon', 'course_banner', 'slug', 'overview', 'my_levels', 'course_faqs']
    

class ScheduleTimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleTiming
        fields = ['id', 'day', 'start_time', 'end_time']



class ScheduleSerializer(serializers.ModelSerializer):
    timing = ScheduleTimingSerializer(many=True, read_only=True)
    to_course = CourseSerializer(many=False, read_only=True)
    class Meta:
        model = Schedule
        fields = ('id', 'schedule_name', 'start_date', 'end_date', 'seats_left', 'timing', 'to_course')
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        current_date = date.today()
        
        if instance.end_date < current_date:
            """If end date has passed, return an empty representation"""
            representation = {}
        
        return representation   