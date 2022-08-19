# from datetime import datetime, timedelta

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from accounts.models import Appointment
from accounts.choices import AppointmentStatus

from vendors.zoom import Zoom

from .models import Meeting


@receiver(post_save, sender=Appointment)
def post_save_appointment(sender, instance, **kwargs):
    appointment = instance

    # when transitioning from not approved to approved, create a Zoom user if necessary
    if appointment.status == AppointmentStatus.CONFIRMED and not hasattr(
        appointment, "meeting"
    ):
        print("try to make a zoom meeting")
        # don't try to schedule a zoom meeting unless a doctor and patient are connected to the appointment
        if all([appointment.doctor, appointment.patient]):
            zoom_details = Zoom().create_meeting(
                appointment.doctor.zoom_proxy_email_address,
                appointment.patient.email,
                appointment.pk,
                duration=appointment.duration,
                timezone=str(appointment.doctor.timezone),
            )

            meeting, _ = Meeting.objects.get_or_create(
                appointment=appointment,
                doctor=appointment.doctor,
                patient=appointment.patient,
                zoom_id=zoom_details.get("id"),
                # the zoom start URL will be valid for 90 days. If we need to schedule meetings farther out than that, we'll
                # need to refresh the start URL before attempting to start the meeting
                zoom_start_url=zoom_details.get("start_url"),
                zoom_join_url=zoom_details.get("join_url"),
            )
