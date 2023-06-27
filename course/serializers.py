# from django.template.defaultfilters import floatformat, currency
from rest_framework import serializers
from .models import Course, Levels, Plans




class PlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plans
        fields = ['id', 'name', 'description', 'actual_price', 'original_price']

class LevelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Levels
        fields = ['id', 'name', 'description', 'num_classes', 'frequency', 'duration', 'starts_from']

class CourseSerializer(serializers.ModelSerializer):
    my_levels = LevelsSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ['id', 'name', 'slug', 'overview', 'my_levels']