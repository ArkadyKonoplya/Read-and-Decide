from rest_framework import serializers
from .models import Meeting


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'
        read_only_fields = [
            'appointment',
            'doctor',
            'patient',
            'zoom_id',
            'zoom_password',
        ]


class CreateMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['appointment']  # ['date', 'duration']
