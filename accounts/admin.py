from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.token_blacklist import models
from rest_framework_simplejwt.token_blacklist.admin import (
    OutstandingTokenAdmin as BaseOutstandingTokenAdmin,
)

from accounts.models import (
    Appointment,
    CommunityResource,
    ConsultRequest,
    Doctor,
    InsurancePlan,
    Invitation,
    LockedResource,
    Patient,
    Pharmacy,
    Prescription,
    ReferralRequest,
    ReferralRequestResponse,
    Relationship,
    Symptom,
    User,
    TelepsycrxUpload,
    TelepsycrxDownload,
    AnnotatedResponse,
    RescheduleAppointment,
    # PatientUpload,
)
# from accounts.models import User, Patient, Relationship, Invitation, Doctor, InsurancePlan, Pharmacy, Appointment, \
#     Symptom, Prescription, CommunityResource, LockedResource, TelepsycrxUpload, ConsultRequest, ReferralRequest


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            _("Personal info"),
            {
                "fields": (
                    "image",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "type",
                )
            },
        ),
        (_("Profile"), {"fields": ("doctors", "patients")}),
        (
            _("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser"),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (
            _("Validation"),
            {
                "fields": (
                    "activation_token",
                    "activation_expired",
                    "phone_activation_token",
                    "phone_activation_expired",
                    "password_reset_token",
                    "password_reset_expired",
                )
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "type")
    list_filter = ("type",)
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, UserAdmin)
admin.site.register(Patient)
admin.site.register(Relationship)
admin.site.register(Invitation)
admin.site.register(Doctor)
admin.site.register(InsurancePlan)
admin.site.register(Pharmacy)
admin.site.register(Appointment)
admin.site.register(Symptom)
admin.site.register(Prescription)
admin.site.register(CommunityResource)
admin.site.register(LockedResource)
admin.site.register(TelepsycrxUpload)
admin.site.register(TelepsycrxDownload)
admin.site.register(ReferralRequest)
admin.site.register(ReferralRequestResponse)
admin.site.register(ConsultRequest)
admin.site.register(AnnotatedResponse)
admin.site.register(RescheduleAppointment)


class OutstandingTokenAdmin(BaseOutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True


admin.site.unregister(models.OutstandingToken)
admin.site.register(models.OutstandingToken, OutstandingTokenAdmin)
admin.site.unregister(Group)
