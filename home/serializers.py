from rest_framework import serializers

from .models import FAQs

class FAQsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQs
        fields = ['question', 'answer']