from rest_framework import serializers
# from rest_framework.request import Request
from telepsycrx_marketing.models import UserSuggestion, UserReview, DoctorWaitList, PatientWaitList


class UserSuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSuggestion
        fields = ('url',
                  'id',
                  'date_submitted',
                  'made_by',
                  'user_type',
                  'title',
                  'details')

class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReview
        fields = ('url',
                  'id',
                  'date_submitted',
                  'made_by',
                  'user_type',
                  'title',
                  'details')


class DoctorWaitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorWaitList
        fields = ('url',
                  'id',
                  'user',
                  'doctor_id',
                  'first_name',
                  'last_name',
                  'email',
                  'state_of_residence',
                  'states_of_license',
                  'is_active')

class PatientWaitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientWaitList
        fields = ('url',
                  'id',
                  'user',
                  'patient_id',
                  'first_name',
                  'last_name',
                  'email',
                  'state_of_residence',
                  'is_active')