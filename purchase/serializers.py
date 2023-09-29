from datetime import datetime, timedelta
from rest_framework import serializers
from .models import Purchase, PurchaseSession
from course.serializers import LevelsSerializer, ScheduleSerializer, PlansSerializer
from user.serializers import kidInfoSerializer

class PurchaseSerializer(serializers.ModelSerializer):
    course_level  = LevelsSerializer(many=False, read_only=True)
    schedule      = ScheduleSerializer(many=False, read_only=True)
    plan_selected = PlansSerializer(many=False, read_only=True)
    kids_selected = kidInfoSerializer(many=True, read_only=True)    
    course_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Purchase
        fields = [
            'course_level', 'schedule', 'plan_selected', 'purchase_price',
            'kids_selected', 'order_id', 'payment_method', 'payment_platform', 'total_sessions', 'completed_sessions',
            'booking_id', 'course_status'
            ]
    
    def to_representation(self, instance):
        if instance.payment_status == 'PAID':
            return super().to_representation(instance)
        else:
            return None


    def get_course_status(self, obj):
        course_status = 'Not Yet Started'
        completed_sessions = obj.completed_sessions
        total_sessions     = obj.total_sessions
        if completed_sessions < total_sessions and completed_sessions != 0:
            course_status = 'ongoing'

        if completed_sessions == total_sessions and completed_sessions != 0:
            course_status = 'completed'

        return course_status
    
class PurchaseSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseSession
        fields = '__all__'
    