from rest_framework import serializers
# from rest_framework.request import Request

from .models import Billing, Transaction

from accounts.serializers import UserSerializer


class BillingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    date = serializers.DateField()
    transaction_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Billing
        fields = [
            'url',
            'id',
            'user',
            'user_id',
            'date',
            'amount',
            'transaction_set',
        ]


class TransactionSerializer(serializers.ModelSerializer):
    billing = BillingSerializer(read_only=True)
    billing_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    time = serializers.DateTimeField()
    txn_id = serializers.CharField(read_only=True)

    class Meta:
        model = Transaction
        fields = ('url',
                  'id',
                  'billing',
                  'billing_id',
                  'user',
                  'user_id',
                  'time',
                  'amount',
                  'type',
                  'status',
                  'txn_id')
