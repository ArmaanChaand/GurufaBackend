from datetime import datetime
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Kid
from .validators import password_validator
from purchase.models import Purchase
from course.models import Levels, Course   


class userInfoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = [
            'id', 'first_name','last_name','email', 
            'phone_number', 'whatsapp_update',
            'is_email_verified', 'is_phone_verified', 'last_name','email', 'phone_number',
            'picture', 'auth_provider_img',
            'auth_providers','is_a_guru','user_roles',  
            'is_active', 'reviewed_courses_list', 'purchased_courses_list',
            # 'password'
            ]
        # fields = '__all__'    
    
        
class registerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'phone_number', 'password', 'whatsapp_update']
        extra_kwargs = {
            'password': {'write_only': True},
        }


    def validate_password(self, value):
        """
            Check Passowrd's strength
        """
        is_strong = password_validator(value)
        if is_strong[0]:
            return value
        else:
            raise serializers.ValidationError(is_strong[1])
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        return super().create(validated_data)

class CourseSerializerSmall(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name','course_icon', 'slug']

class KidsPurchaseLevelsSerializer(serializers.ModelSerializer):
    to_course = CourseSerializerSmall(many=False, read_only=True)
    class Meta:
        model = Levels
        fields = ['id', 'name', 'description', 'to_course']


class KidsPurchaseSerializer(serializers.ModelSerializer):
    course_level = KidsPurchaseLevelsSerializer(many=False, read_only=True)
    course_status = serializers.SerializerMethodField()

    class Meta:
        model = Purchase
        fields = ['course_level', 'schedule', 'plan_selected', 'booking_id',
                'purchase_price', 'kids_selected', 'total_sessions', 'completed_sessions', 'course_status']

    
    def get_course_status(self, obj):
        course_status = 'Not Yet Started'
        completed_sessions = obj.completed_sessions
        total_sessions     = obj.total_sessions
        if completed_sessions < total_sessions and completed_sessions != 0:
            course_status = 'ongoing'

        if completed_sessions == total_sessions and completed_sessions != 0:
            course_status = 'completed'

        return course_status
    
    def to_representation(self, instance):
        if instance.payment_status == 'PAID':
            return super().to_representation(instance)  
        else:
            return None
    

class kidInfoSerializer(serializers.ModelSerializer):
    my_purchases = KidsPurchaseSerializer(many=True, read_only=True)
    class Meta: 
        model = Kid
        fields = ['id', 'kid_profile','kid_first_name','kid_last_name', 'kid_age', 'my_purchases', 'kid_gender', 'demo_courses']
    
    def validate_kid_profile(self, value):
        if value and value.size > 2 * 1024 * 1024:  
            raise serializers.ValidationError("Image size should be less than 2MB.")
        return value
    