from rest_framework import serializers
from .models import User, Kid
from .validators import password_validator
from django.contrib.auth.hashers import make_password


class userInfoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['first_name','last_name','email']

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



class kidInfoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Kid
        fields = ['id', 'kid_profile','kid_first_name','kid_last_name', 'kid_age']
    
    def validate_kid_profile(self, value):
        if value.size > 500 * 1024:  
            raise serializers.ValidationError("Image size should be less than 500KB.")
        return value

"""
admin@gurufa.com
admin@gurufa123
"""