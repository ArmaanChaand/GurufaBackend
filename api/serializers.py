from rest_framework import serializers
from django.conf import settings

class ImageURLwithDomain(serializers.ImageField):
    def to_representation(self, value):
        DOMAIN = settings.HOST
        url = super().to_representation(value)
        if url:
            if not url.startswith('http'):
                return f"{DOMAIN}{url}"
            else:
                return url
        else:
            return None