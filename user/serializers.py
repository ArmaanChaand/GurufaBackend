from rest_framework import serializers
from .models import User
from .validators import password_validator
class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class userInfoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['first_name', 'email']

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

"""
{
    "first_name": "Armaan",
    "last_name": "Chaand",
    "email": "phone@email.com",
    "phone_number": "3234834987",
    "password": "32348sdfsdfj"
}
"""