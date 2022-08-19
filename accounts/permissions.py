from rest_framework.permissions import BasePermission
from .models import Doctor, Patient


# users only access their own data
class IsTheSameUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.id


class IsDoctor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.get('email'):
            doctor = Doctor.objects.filter(email=request.user.email)
            return doctor.exists()
        return False


class IsPatient(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.get('email'):
            patient = Patient.objects.filter(email=request.user.email)
            return patient.exists()
        return False
