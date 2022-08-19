from django.urls import path
from rest_framework import routers

# from .views import MeetingViewSet, recordingView
from .views import recordingView


router = routers.DefaultRouter()
# router.register('meetings', MeetingViewSet)

urlpatterns = router.urls + [path("recordings", recordingView)]
