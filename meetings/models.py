from django.utils import timezone
from django.db import models
from datetime import timedelta
from accounts.models import Appointment, Doctor, Patient


class RecordingStatus(models.TextChoices):
    NOT_AVAILABLE = "Not Available"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    ERROR = "Error"


class Meeting(models.Model):
    appointment = models.OneToOneField(
        Appointment, on_delete=models.CASCADE, primary_key=True
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING)
    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING)
    zoom_id = models.CharField(max_length=64)
    zoom_password = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    session_start = models.DateTimeField(null=True, blank=True)
    session_duration = models.IntegerField(default=0)
    recording_url = models.CharField(max_length=150, null=True, blank=True)
    recording_status = models.CharField(
        max_length=20,
        choices=RecordingStatus.choices,
        default=RecordingStatus.NOT_AVAILABLE,
    )
    zoom_start_url = models.URLField(max_length=512, null=True, blank=True)
    zoom_join_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Appt {self.appointment.id} Zoom id {self.zoom_id}"
