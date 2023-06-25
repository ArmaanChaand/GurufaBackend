from rest_framework import serializers
from .models import Course, Levels

class LevelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Levels
        fields = ['id', 'name', 'num_classes', 'frequency', 'duration']

class CourseSerializer(serializers.ModelSerializer):
    my_levels = LevelsSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ['id', 'name', 'slug', 'overview', 'my_levels']