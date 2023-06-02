from rest_framework import serializers
from .models import User

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class userInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name']

class registerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'phone_number', 'password', 'whatsapp_update']
        extra_kwargs = {
            'password': {'write_only': True},
        }

"""
{
    "first_name": "Armaan",
    "last_name": "Chaand",
    "email": "phone@email.com",
    "phone_number": "3234834987",
    "password": "32348sdfsdfj"
}
"""