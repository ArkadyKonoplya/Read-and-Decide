# from django.urls import path
from rest_framework import routers
from django.urls import path

from .views import (
    BillingViewSet,
    TransactionViewSet,
)

router = routers.DefaultRouter()
router.register('billings', BillingViewSet)
router.register('transactions', TransactionViewSet)

urlpatterns = router.urls
