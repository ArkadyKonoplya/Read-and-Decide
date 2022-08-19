from rest_framework import serializers
# from rest_framework.request import Request
from telepsycrx_hr.models import UserConcern


class UserConcernSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConcern
        fields = ('url',
                  'id',
                  'date_submitted',
                  'made_by',
                  'user_type',
                  'title',
                  'details',
                  'is_resolved',
                  'files_requested_by_telepsycrx')