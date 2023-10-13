from rest_framework import serializers

from .models import FAQs, Review, CustomerOperations
from user.serializers import userInfoSerializer

class FAQsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQs
        fields = ['question', 'answer']

class ReviewSerializer(serializers.ModelSerializer):
    review_by = userInfoSerializer(many=False, read_only=True)
    created_at = serializers.DateTimeField(format='%d/%m/%Y', read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'

class CustomerOperationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerOperations
        fields = ['email', 'phone', 'message']
    