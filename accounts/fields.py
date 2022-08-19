from datetime import datetime

from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField as BasePhoneNumberField
from django.utils import timezone


class PhoneNumberField(BasePhoneNumberField):
    def to_representation(self, value):
        if not value:
            return ''

        return str(value.national_number)

    def to_internal_value(self, data):
        if '+' not in data:
            data = f'+1{data}'

        return super().to_internal_value(data)



class DateTimeField(serializers.DateTimeField):
    def to_internal_value(self, value):
        return datetime.fromtimestamp(datetime.fromisoformat(value).timestamp(), timezone.utc)

    def to_representation(self, value):
        if not value:
            return None

        return value.timestamp()
