from rest_framework import serializers
from .models import Idea, Feedback,DigiLockerProfile


class IdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idea
        exclude = ['user']  # don't expect user from client
        extra_kwargs = {
            'audio_file': {'required': False, 'allow_null': True}
        }

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class DigiLockerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigiLockerProfile
        fields = '__all__' 