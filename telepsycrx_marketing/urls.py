
# from django.urls import path
from rest_framework import routers

from telepsycrx_marketing.views import (
    UserSuggestionViewSet,
    UserReviewViewSet,
    DoctorWaitListViewSet,
    PatientWaitListViewSet,
)

router = routers.DefaultRouter()
router.register('marketing-suggestions', UserSuggestionViewSet)
router.register('marketing-reviews', UserReviewViewSet )
router.register('doctor-waitlist', DoctorWaitListViewSet )
router.register('patient-waitlist', PatientWaitListViewSet )

urlpatterns = [

]

urlpatterns += router.urls

