from rest_framework import serializers

from .models import Purchase
from course.serializers import LevelsSerializer, ScheduleSerializer, PlansSerializer
from user.serializers import kidInfoSerializer

class PurchaseSerializer(serializers.ModelSerializer):
    course_level  = LevelsSerializer(many=False, read_only=True)
    schedule      = ScheduleSerializer(many=False, read_only=True)
    plan_selected = PlansSerializer(many=False, read_only=True)
    kids_selected = kidInfoSerializer(many=True, read_only=True)
    class Meta:
        model = Purchase
        fields = ['course_level', 'schedule', 'plan_selected', 'purchase_price', 'kids_selected']
    