from django.urls import path
from rest_framework import routers


from .views import (
    AppointmentViewSet,
    BlacklistTokenUpdateView,
    CustomUserCreate,
    PatientViewSet,
    UserViewSet,
    DoctorViewSet,
    ValidateNewUser,
    ConsultRequestViewSet,
    AppointmentConfirmationViewSet,
    AssociationViewSet,
    ReferralRequestViewSet,
    ReferralRequestResponseViewSet,
    LockedResourceViewset,
    CommunityResourceViewset,
    TelepsycrxUploadViewset,
    TelepsycrxDownloadViewset,
    AnnotatedResponseViewset,
    RescheduleAppointmentViewSet,
    # FileView
)

app_name = "accounts"

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('appointments', AppointmentViewSet)
router.register('reschedule-appointments', RescheduleAppointmentViewSet)
router.register('patients', PatientViewSet)
router.register('doctors', DoctorViewSet)
router.register('consult_requests', ConsultRequestViewSet)
router.register('referral_requests', ReferralRequestViewSet)
router.register('referral_request_responses', ReferralRequestResponseViewSet)
router.register('confirmation', AppointmentConfirmationViewSet)
router.register('associations', AssociationViewSet, basename='associations')
router.register('telepsycrx-uploads', TelepsycrxUploadViewset)
router.register('telepsycrx-downloads', TelepsycrxDownloadViewset)
router.register('patient-res', LockedResourceViewset)
router.register('annotated-res', AnnotatedResponseViewset)
# router.register('patient-uploads', LockedResourceViewset)
router.register('comm-res', CommunityResourceViewset)
# router.register('get_upload_url', FileView.as_view(), basename='get_upload_url')

urlpatterns = router.urls

#  creating and logging out users
urlpatterns += [
    path("create/", CustomUserCreate.as_view(), name="create_user"),
    path("logout/blacklist/", BlacklistTokenUpdateView.as_view(), name="blacklist"),
    path("validate-new-user/", ValidateNewUser.as_view(), name="validate_new_user"),
]
