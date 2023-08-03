from rest_framework import serializers
from .models import BecomeAGuru

class BecomeAGuruSerializer(serializers.ModelSerializer):
    class Meta:
        model = BecomeAGuru
        fields = '__all__'