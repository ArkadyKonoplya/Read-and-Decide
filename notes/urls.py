# from django.urls import path
from rest_framework import routers
from django.urls import path

from notes.views import (
    ProviderNoteViewSet,
    DownloadViewSet
)

router = routers.DefaultRouter()
router.register('provider-notes', ProviderNoteViewSet, basename='provider-notes')

urlpatterns = [
    path('pdf/<pk>/', DownloadViewSet.as_view(), name='pdf'),
]

urlpatterns += router.urls
