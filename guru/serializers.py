from rest_framework import serializers, fields
from .models import BecomeAGuru, SKILLS_CHOICES

def validate_skills(value):
    if not value:
        raise serializers.ValidationError("At least one skill must be selected.")
    return value

class BecomeAGuruSerializer(serializers.ModelSerializer):
    skills = fields.MultipleChoiceField(choices=SKILLS_CHOICES, validators=[validate_skills])
    class Meta:
        model = BecomeAGuru
        fields = '__all__'


"""
{
  "full_name": "John Doe",
  "email": "john.doe@example.com",
  "phone_number": "8210485920",
  "yrs_experience": "5.5",
  "skills": ["Chess", "Other"],
  "other_skills": "Some other skill"
}

"""