from rest_framework import serializers

from .models import Purchase

class PurchaseSerializer(serializers.Serializer):
    class Meta:
        model = Purchase
        fields = ['dummy']