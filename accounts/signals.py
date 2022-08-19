from datetime import datetime, timedelta

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.template import Template
from django.template.loader import get_template

from .models import User, Appointment, Prescription, Doctor
from .utils import send_email
from notes.models import ProviderNote
from personal_journal.models import JournalEntry


@receiver(user_logged_in)
def on_login(sender, user, request, **kwargs):
    """
    This function is called when a user logs in.
    """
    # for entry in JournalEntry.objects.filter(author=user, archived=False):
    #     if entry.created_at.date() < user.profile.last_login.date() - timedelta(days=7):
    #         entry.status = 'Archived'
    #         entry.archived = True
    #         entry.save()

    for entry in ProviderNote.objects.filter(author=user, archived=False):
        if entry.date_created.date() < user.last_login.date() - timedelta(days=7):
            # entry.status = 'Archived'
            entry.archived = True
            entry.save()

    #TODO: Filter appointments by doctor or patient ID
    # for appointment in Appointment.objects.filter(LinkIsActive=True):
    #     if appointment.created_at.date() < user.profile.last_login.date() - timedelta(days=7):
    #         appointment.LinkIsActive = False
    #         appointment.save()


@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, **kwargs):
    if not created:
        return
    instance.notify()


@receiver(pre_save, sender=Doctor)
def pre_save_doctor(sender, instance, **kwargs):
    if instance.is_approved and not instance.zoom_user_id:
        instance.zoom_user_id = instance.zoom_proxy_email_address


@receiver(post_save, sender=Appointment)
def post_save_appointment(sender, instance, **kwargs):
    subject: str = ''
    user: User = None
    date: datetime = instance.date
    template: Template = None

    if instance.status == 'Requested':
        subject = f'Appointment Request from {instance.patient}'
        user = User.objects.get(email=instance.doctor.email)
        template = get_template('alerts/requested.html')
    elif instance.status == 'Confirmed':
        subject = f'Confirmation of Appointment Request from {instance.doctor}'
        user = User.objects.get(email=instance.patient.email)
        template = get_template('alerts/confirmed.html')
    elif instance.status == 'Rescheduled':
        subject = f'Re-schedule Appointment Request from {instance.doctor}'
        user = User.objects.get(email=instance.patient.email)
        template = get_template('alerts/rescheduled.html')
    elif instance.status == 'Denied':
        subject = f'Appointment denied from {instance.doctor}'
        user = User.objects.get(email=instance.patient.email)
        template = get_template('alerts/denied.html')

    content = template.render({
        'appointment': instance,
        'patient': instance.patient,
        'provider': instance.doctor,
        'confirm_url': '{}/api/accounts/appointments/{}/confirm'.format(settings.BACKEND_BASE_URL, instance.pk),
        'deny_url': '{}/api/accounts/appointments/{}/deny'.format(settings.BACKEND_BASE_URL, instance.pk),
        'date': date.astimezone(instance.doctor.timezone).strftime(
            f'%Y-%m-%d %H:%M {instance.doctor.timezone.tzname(datetime.now())}'),
    })
    send_email(subject, content, user)


@receiver(post_save, sender=Appointment)
def send_appointment_request_mail(sender, instance, created, **kwargs):
    if not created:
        return
    subject, from_email, to , pk = 'Appointment Request', 'TelePsycRX@telepsycrx.com', instance.patient.email, instance.id
    text_content = 'You have an appointment request.'
    doc = instance.doctor.first_name
    html_content = f'<p>You have an appointment request from Doctor {doc}</p><a href="http://127.0.0.1:8000/api/accounts/appointments/confirm_appointment/?pk=' + str(pk) + '">Confirm </a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="http://127.0.0.1:8000/api/accounts/appointments/' + str(pk) + '">Reschedule</a>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

# @receiver(post_save, sender=Prescription)
# def post_save_prescription(sender, instance, created, **kwargs):
#     if not created:
#         return

#     subject = 'Prescription from TelepsycRX'
#     template = get_template('prescription.html')
#     content = template.render({
#         'date': instance.date_created.strftime(f'%Y-%m-%d %H:%M:%S {instance.doctor.timezone.tzname(datetime.datetime.now())}'),
#         'prescription': instance,
#     })

#     send(subject, content)

