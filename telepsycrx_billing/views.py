from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.conf import settings


from .serializers import BillingSerializer, TransactionSerializer
from .models import Billing, Transaction


class BillingViewSet(ModelViewSet):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer
    permission_classes = (permissions.IsAdminUser,)


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAdminUser,)

    # @action(detail=False, methods=['post'])
    # def converge_sale(self, request, format=None):
    #     converge = Converge(settings.CONVERGE_MERCHANT_ID, settings.CONVERGE_USER_ID,
    #                         settings.CONVERGE_PIN, is_demo=settings.CONVERGE_DEMO)

    #     data = {
    #         'ssl_amount': request.data.get('amount'),
    #     }
    #     response = converge.request('ccgettoken', **data)

    #     # TODO: Create a transaction record

    #     return Response(response)
