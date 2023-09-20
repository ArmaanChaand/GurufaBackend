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

    total_sessions = serializers.SerializerMethodField()
    completed_sessions = serializers.SerializerMethodField()
    
    class Meta:
        model = Purchase
        fields = [
            'course_level', 'schedule', 'plan_selected', 'purchase_price',
            'kids_selected', 'order_id', 'payment_method', 'payment_platform', 'total_sessions', 'completed_sessions',
            'booking_id'
            ]
    
    def to_representation(self, instance):
        if instance.payment_status == 'PAID':
            return super().to_representation(instance)
        else:
            return None
    
    def get_total_sessions(self, obj):
        # Count the total number of ScheduleTimings associated with the purchase's schedule
        return obj.schedule.timing.count()

    def get_completed_sessions(self, obj):
        # Count the number of completed ScheduleTimings associated with the purchase's schedule
        now = datetime.now().time()
        return obj.schedule.timing.filter(date__lte=datetime.now().date(), end_time__lt=now).count() # Count today
        # return obj.schedule.timing.filter(date__lt=datetime.now().date(), end_time__lt=now).count() # Omit today
    
class PurchaseSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseSession
        fields = '__all__'
    