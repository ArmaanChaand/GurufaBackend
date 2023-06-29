from rest_framework import serializers
from .models import Course, Levels, Plans, Batch, BatchTiming
from home.serializers import FAQsSerializer
from datetime import date


class PlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plans
        fields = ['id', 'name','slug', 'description', 'actual_price', 'original_price', 'count_sibling']

class LevelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Levels
        fields = ['id', 'name', 'description', 'num_classes', 'frequency', 'duration', 'starts_from']

class CourseSerializer(serializers.ModelSerializer):
    my_levels = LevelsSerializer(many=True, read_only=True)
    course_faqs = FAQsSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ['id', 'name','course_icon', 'course_banner', 'slug', 'overview', 'my_levels', 'course_faqs']
    

class BatchTimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchTiming
        fields = ['id', 'day', 'start_time', 'end_time']



class BatchSerializer(serializers.ModelSerializer):
    timing = BatchTimingSerializer(many=True, read_only=True)
    class Meta:
        model = Batch
        fields = ('id', 'batch_name', 'start_date', 'end_date', 'seats_left', 'timing')
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        current_date = date.today()
        
        if instance.end_date < current_date:
            # If end date has passed, return an empty representation
            representation = {}
        
        return representation   