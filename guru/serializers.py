from rest_framework import serializers, fields
from .models import BecomeAGuru, SKILLS_CHOICES, Guru

def validate_skills(value):
    if not value:
        raise serializers.ValidationError("At least one skill must be selected.")
    return value

class BecomeAGuruSerializer(serializers.ModelSerializer):
    skills = fields.MultipleChoiceField(choices=SKILLS_CHOICES, validators=[validate_skills])
    class Meta:
        model = BecomeAGuru
        fields = '__all__'

class GuruSerializerForSchedule(serializers.ModelSerializer):
    # Define fields from the linked User model
    first_name = serializers.CharField(source='user_id.first_name', read_only=True)
    last_name = serializers.CharField(source='user_id.last_name', read_only=True)
    picture = serializers.CharField(source='user_id.picture', read_only=True)
    auth_provider_img = serializers.CharField(source='user_id.auth_provider_img', read_only=True)

    class Meta:
        model = Guru
        fields = ['id', 'is_active', 'guru_description', 'experience', 'first_name', 'last_name', 'picture', 'auth_provider_img']
