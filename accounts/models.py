import binascii
from operator import mod
import os
import random
import datetime

from django.conf import settings
from django.db.models.deletion import CASCADE, DO_NOTHING, PROTECT
from config.settings import CLIENT
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField  # This is specific to Postgres
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models.fields import IntegerField
from django.db.models.fields.files import ImageField
from django.template.loader import get_template
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from timezone_field import TimeZoneField
# from accounts.serializers import FileSerializer
# from storages.backends.s3boto import S3BotoStorage

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives


from .choices import (
    UserType,
    Gender,
    HeightUnit,
    WeightUnit,
    RelationshipType,
    InvitationStatus,
    TITLES,
    AppointmentStatus,
    SubscriptionType,
    Duration,
    Recurring,
)
# from .twilio import client, messaging_service_sid
from .managers import UserManager
from vendors.zoom import Zoom


def upload_to(instance, filename):
    return "profile_pics/{filename}".format(filename=filename)


class User(AbstractUser):
    username = None
    # image = ImageField(
    #     _("images"), default="default.jpg", upload_to=upload_to, null=True, blank=True
    # )
    # email = models.EmailField(_("email address"), unique=True)
    # date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    # type = models.CharField(max_length=20, choices=UserType.choices, default="Patient")
    image = ImageField(_('images'), default='default.jpg', upload_to='profile_pics', null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    type = models.CharField(max_length=20, choices=UserType.choices, default='Patient')
    phone_number = PhoneNumberField(null=True, blank=True)
    doctors = models.ManyToManyField("Doctor", blank=True)
    patients = models.ManyToManyField("Patient", blank=True)
    activation_token = models.CharField(max_length=6, null=True, blank=True)
    activation_expired = models.DateTimeField(null=True, blank=True)
    phone_activated = models.BooleanField(default=False, blank=True)
    phone_activation_token = models.CharField(max_length=6, null=True, blank=True)
    phone_activation_expired = models.DateTimeField(null=True, blank=True)
    password_reset_token = models.CharField(max_length=6, null=True, blank=True)
    password_reset_expired = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)  # Added for authentication

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    #  def save(self, *args, **kwargs):
    #     if self.image:
    #         self.image = get_thumbnail(self.image, '500x600', quality=99, format='JPEG')
    #     super(MyPhoto, self).save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name()

    def notify(self):
            self.send_activation_token()
            self.send_phone_activation_token()

    def send_activation_token(self):
       
        # TODO: fix me
        # need to be able to mock these so they don't send via the test suite
        self.activation_token = str(binascii.hexlify(os.urandom(3)), "ascii").upper()
        self.activation_expired = timezone.now() + timezone.timedelta(minutes=30)
        self.save(update_fields=["activation_token", "activation_expired"])

        subject = "Please confirm your email address"
        to = [self.email]

        template = get_template("alerts/creation.html")
        content = template.render(
            {
                "name": str(self),
                "email": self.email,
                "code": self.activation_token,
            }
        )
        msg = EmailMultiAlternatives(subject, "", settings.DEFAULT_FROM_EMAIL, to)
        msg.attach_alternative(content, "text/html")
        msg.content_subtype = "html"
        msg.send(fail_silently=False)
        print("END SENDING EMAIL**************************")

    def send_phone_activation_token(self):
       
        # TODO: fix me
        # need to be able to mock these so they don't send via the test suite
        self.phone_activation_token = f"{random.randrange(1, 10**6):06}"
        self.phone_activation_expired = timezone.now() + timezone.timedelta(minutes=30)
        self.save(update_fields=["phone_activation_token", "phone_activation_expired"])

        CLIENT.publish(
            PhoneNumber=str(self.phone_number),
            Message=f"Your TelepsycRX code is {self.phone_activation_token}",
        )
        print("END SENDING TEXT message**************************")

        # BELOW IS OLD CODE:
        # client.messages.create(messaging_service_sid=messaging_service_sid,
        #                        body=f'Your TelepsycRX code is {self.phone_activation_token}',
        #                        to=self.phone_number.raw_input)

    def send_password_reset_token(self):
        self.password_reset_token = str(
            binascii.hexlify(os.urandom(3)), "ascii"
        ).upper()
        self.password_reset_expired = timezone.now() + timezone.timedelta(minutes=30)
        self.save(update_fields=["password_reset_token", "password_reset_expired"])

        subject = "Password Reset"
        to = [self.email]

        template = get_template("alerts/password_reset.html")
        content = template.render(
            {
                "email": self.email,
                "token": self.password_reset_token,
            }
        )
        msg = EmailMultiAlternatives(subject, "", settings.DEFAULT_FROM_EMAIL, to)
        msg.attach_alternative(content, "text/html")
        msg.content_subtype = "html"
        msg.send(fail_silently=False)

        # @property
        # def key(self):
        #     obj = FileSerializer.save()
        # # for the sake of simplicity; assuming that all files have the format <name>.<ext>. Files without extension would error here.
        #     return str(obj.id) + '-' + FileSerializer.data['name'].split('.')[0] + '/' + FileSerializer.data['name']


class InsurancePlan(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Patient(models.Model):
    is_subscribed = models.BooleanField(null=True)
    is_identified = models.BooleanField(null=True, default=False)
    freemium_doc_array = ArrayField(models.CharField(max_length=20), default=list, null=True, blank=True)
    # is_on_waitList = models.BooleanField(null=True)
    # past_doctors = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    # current_doctors = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    subscription_type = models.CharField(
        max_length=70, choices=SubscriptionType.choices, null=True, blank=True
    )
    isUsingDelivery = models.BooleanField(default=False)
    email = models.EmailField(_("email address"))
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    phone_number = PhoneNumberField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=20, choices=Gender.choices, null=True, blank=True
    )
    address1 = models.CharField(max_length=200, null=True, blank=True)
    address2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    zip = models.CharField(max_length=10, null=True, blank=True)
    insurance_plan_username = models.CharField(max_length=50)
    pharmacy_plan = models.CharField(max_length=20, null=True, blank=True)
    pharmacy_member = models.CharField(max_length=20, null=True, blank=True)
    pharmacy_bin = models.CharField(max_length=20, null=True, blank=True)
    height_ft = models.IntegerField(default=00)
    height_inch = models.IntegerField(default=00)
    height = models.FloatField(null=True, blank=True)
    # height_unit = models.CharField(
    #     max_length=2, choices=HeightUnit.choices, default=HeightUnit.FT
    # )
    # weight = models.FloatField(null=True, blank=True)
    # weight_unit = models.CharField(
    #     max_length=2, choices=WeightUnit.choices, default=WeightUnit.LB
    # )
    height_unit = models.CharField(max_length=2, choices=HeightUnit.choices, default=HeightUnit.FT)
    weight = models.CharField(max_length=20, default='000')
    weight_unit = models.CharField(max_length=2, choices=WeightUnit.choices, default=WeightUnit.LB)
    medications = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    allergies = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    smoke = models.BooleanField(default=False)
    alcohol = models.BooleanField(default=False)
    asthma = models.BooleanField(default=False)
    kidney_problems = models.BooleanField(default=False)
    high_blood_pressure = models.BooleanField(default=False)
    low_blood_pressure = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    heart_problems = models.BooleanField(default=False)
    headaches = models.BooleanField(default=False)
    urinary_tract_infections = models.BooleanField(default=False)
    depression = models.BooleanField(default=False)
    seizures = models.BooleanField(default=False)
    stroke = models.BooleanField(default=False)
    thyroid_disease = models.BooleanField(default=False)
    arrhythmias = models.BooleanField(default=False)
    anxiety = models.BooleanField(default=False)
    panic_attacks = models.BooleanField(default=False)
    copd = models.BooleanField(default=False)
    eczema = models.BooleanField(default=False)
    psoriasis = models.BooleanField(default=False)
    cancer = models.BooleanField(default=False)
    other_problems = models.CharField(max_length=200, null=True, blank=True)
    family_asthma = models.BooleanField(default=False)
    family_stroke = models.BooleanField(default=False)
    family_diabetes = models.BooleanField(default=False)
    family_heart_problems = models.BooleanField(default=False)
    family_high_blood_pressure = models.BooleanField(default=False)
    family_low_blood_pressure = models.BooleanField(default=False)
    family_thyroid_disease = models.BooleanField(default=False)
    family_arrhythmias = models.BooleanField(default=False)
    family_anxiety = models.BooleanField(default=False)
    family_panic_attacks = models.BooleanField(default=False)
    family_copd = models.BooleanField(default=False)
    family_eczema = models.BooleanField(default=False)
    family_psoriasis = models.BooleanField(default=False)
    family_headaches = models.BooleanField(default=False)
    family_seizures = models.BooleanField(default=False)
    family_depression = models.BooleanField(default=False)
    family_kidney_problems = models.BooleanField(default=False)
    family_urinary_tract_infections = models.BooleanField(default=False)
    family_cancer = models.BooleanField(default=False)
    family_other_problems = models.CharField(max_length=200, null=True, blank=True)
    # activation_token = models.CharField(max_length=6, null=True, blank=True)
    # activation_expired = models.DateTimeField(null=True, blank=True)
    # phone_activation_token = models.CharField(max_length=6, null=True, blank=True)
    # phone_activation_expired = models.DateTimeField(null=True, blank=True)

    # insurance_plan = models.ForeignKey(
    #     InsurancePlan, null=True, blank=True, on_delete=models.SET_NULL
    # )
    insurance_plan = models.ForeignKey(InsurancePlan, null=True, blank=True, on_delete=models.SET_NULL)
    local_pharmacy = models.ForeignKey("Pharmacy", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Relationship(models.Model):
    relationship = models.CharField(
        max_length=20, choices=RelationshipType.choices, default="Me"
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} ({self.relationship})"


class Invitation(models.Model):
    relationship = models.CharField(max_length=20, choices=RelationshipType.choices)
    email = models.EmailField()
    # first_name = models.CharField(_("first name"), max_length=150)
    # last_name = models.CharField(_("first name"), max_length=150)
    # status = models.CharField(
    #     max_length=10,
    #     choices=InvitationStatus.choices,
    #     default=InvitationStatus.INVITED,
    # )
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    status = models.CharField(max_length=10, choices=InvitationStatus.choices, default=InvitationStatus.INVITED)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}'s {self.relationship} ({self.status})"


class Doctor(models.Model):
    doc_partner_patients = ArrayField(models.CharField(max_length=20), default=list, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    is_accepting_new_patients = models.BooleanField(default=True)
    is_partner_account = models.BooleanField(default=False)
    email = models.EmailField()
    title = models.CharField(max_length=36, choices=TITLES, null=True, blank=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    since = models.DateField(null=True, blank=True)
    board_certified_speciality = models.CharField(max_length=200, null=True, blank=True, default='')
    states = ArrayField(models.CharField(max_length=300), null=True, blank=True)
    state_license_numbers = ArrayField(models.CharField(max_length=300), default=list, null=True, blank=True)
    license_pdf_upload = models.FileField(upload_to='doctors/licenses', null=True)
    npi = models.CharField(max_length=20, null=True, blank=True)
    dea = models.CharField(max_length=20, null=True, blank=True)
    address1 = models.CharField(max_length=200, null=True, blank=True)
    address2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    zip = models.CharField(max_length=10, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    fax_number = models.CharField(max_length=50, null=True, blank=True)
    # timezone = TimeZoneField(default="Pacific/Honolulu")
    # office_is_active = models.BooleanField(null=True)
    # sun_start = models.TimeField(default="09:00:00")
    # sun_end = models.TimeField(default="18:00:00")
    timezone = TimeZoneField(default='Pacific/Honolulu')
    office_is_active = models.BooleanField(default=True)
    sun_start = models.TimeField(default='09:00:00')
    sun_end = models.TimeField(default='18:00:00')
    sun_off = models.BooleanField(default=True)
    mon_start = models.TimeField(default="09:00:00")
    mon_end = models.TimeField(default="18:00:00")
    mon_off = models.BooleanField(default=False)
    tue_start = models.TimeField(default="09:00:00")
    tue_end = models.TimeField(default="18:00:00")
    tue_off = models.BooleanField(default=False)
    wed_start = models.TimeField(default="09:00:00")
    wed_end = models.TimeField(default="18:00:00")
    wed_off = models.BooleanField(default=False)
    thu_start = models.TimeField(default="09:00:00")
    thu_end = models.TimeField(default="18:00:00")
    thu_off = models.BooleanField(default=False)
    fri_start = models.TimeField(default="09:00:00")
    fri_end = models.TimeField(default="18:00:00")
    fri_off = models.BooleanField(default=False)
    sat_start = models.TimeField(default="09:00:00")
    sat_end = models.TimeField(default="18:00:00")
    sat_off = models.BooleanField(default=True)
    about = models.TextField(null=True, blank=True)
    # activation_token = models.CharField(max_length=6, null=True, blank=True)
    # activation_expired = models.DateTimeField(null=True, blank=True)
    # phone_activation_token = models.CharField(max_length=6, null=True, blank=True)
    # phone_activation_expired = models.DateTimeField(null=True, blank=True)
    accepting_new_patients = models.BooleanField(default=True)
    zoom_user_id = models.CharField(max_length=64, null=True, blank=True)
    # past_patients = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    # current_patients = ArrayField(models.CharField(max_length=50), blank=True, default=list)

    @property
    def zoom_proxy_email_address(self):
        """
        This shouldn't be used in the application except to provide a fictitious email for Zoom's user registration
        purposes
        """
        return f"{self.pk}@providers.telepsycrx.com"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_is_approved = self.is_approved

    def save(self, *args, **kwargs):
        self.clean()

        # TODO: investigate making this async
        # when transitioning from not approved to approved, create a Zoom user if necessary
        if not self.original_is_approved and self.is_approved and not self.zoom_user_id:
            self.zoom_user_id = Zoom().create_user_account(
                self.zoom_proxy_email_address, self.first_name, self.last_name
            )

        super().save(*args, **kwargs)

    def get_available_times_by_day(self, date=datetime.date.today()):
        if not isinstance(date, datetime.date):
            raise AttributeError("date must be a Python date object")

        # Initialize available slots list
        available_slots = []

        # Determine start and end times for the day
        day_num = date.weekday()
        if day_num == 1:
            start = self.sun_start
            end = self.sun_end
        elif day_num == 2:
            start = self.mon_start
            end = self.mon_end
        elif day_num == 3:
            start = self.tue_start
            end = self.tue_end
        elif day_num == 4:
            start = self.wed_start
            end = self.wed_end
        elif day_num == 5:
            start = self.thu_start
            end = self.thu_end
        elif day_num == 6:
            start = self.fri_start
            end = self.fri_end
        else:
            start = self.sat_start
            end = self.sat_end

        # Fill up available slots for the day
        for hour in range(start.hour, end.hour):
            for minute in range(0, 60, 30):
                time = datetime.time(hour, minute, 0)
                available_slots.append(time)

        # Remove slots that are blocked by existing appointments
        for appointment in self.appointments.filter(status='Confirmed',
                                                    date__year=date.year,
                                                    date__month=date.month,
                                                    date__day=date.day):
            available_slots.remove(appointment.date.time())
            if appointment.duration >= 60:
                available_slots.remove((appointment.date + datetime.timedelta(minutes=30)).time())
            if appointment.duration >= 90:
                available_slots.remove((appointment.date + datetime.timedelta(minutes=60)).time())
            if appointment.duration == 120:
                available_slots.remove((appointment.date + datetime.timedelta(minutes=90)).time())
        for appointment in self.appointments.filter(status='Requested',
                                                    date__year=date.year,
                                                    date__month=date.month,
                                                    date__day=date.day):
            available_slots.remove(appointment.date.time())
            if appointment.duration >= 60:
                available_slots.remove((appointment.date + datetime.timedelta(minutes=30)).time())
            if appointment.duration >= 90:
                available_slots.remove((appointment.date + datetime.timedelta(minutes=60)).time())
            if appointment.duration == 120:
                available_slots.remove((appointment.date + datetime.timedelta(minutes=90)).time())

        return available_slots

    def __str__(self):
        return f"{self.title}. {self.first_name} {self.last_name}"

    # @property
    # def key(self):
    #         obj = FileSerializer.save()
    #     # for the sake of simplicity; assuming that all files have the format <name>.<ext>. Files without extension would error here.
    #         return str(obj.id) + '-' + FileSerializer.data['name'].split('.')[0] + '/' + FileSerializer.data['name']


class Pharmacy(models.Model):
    name = models.CharField(max_length=100)
    address1 = models.CharField(max_length=200, null=True, blank=True)
    address2 = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)
    phone_number = PhoneNumberField()
    fax_number = PhoneNumberField(default="000-000-000")

    def __str__(self):
        return self.name


class Appointment(models.Model):
    requested_by = models.ForeignKey(User, on_delete=PROTECT, null=True)
    date = models.DateTimeField(null=True) 
    allDay = models.BooleanField(default=False)
    duration = models.IntegerField(choices=Duration, default=30)
    requester_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.PATIENT)
    appointment_type = models.CharField(max_length=50, null=True)
    recurring = models.CharField(max_length=50, choices=Recurring.choices, default=Recurring.NO)
    notes = models.JSONField(null=True, blank=True)
    # BELOW: How can the patient questionnaires be saved and accessed?
    questionnaires = models.JSONField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.REQUESTED,
    )
    
    sent = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    is_rescheduled = models.BooleanField(default=False)

    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, null=True, related_name="appointments"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, null=True, related_name="appointments"
    )
    pharmacy = models.ForeignKey(
        Pharmacy, null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.patient} {self.doctor} ({self.date})"

class RescheduleAppointment(models.Model):
    # Ask Comfort if he needs a direct email in this table or if he can extract from the appoinments pk.
    appointment_ref = models.ForeignKey(Appointment, on_delete=PROTECT, null=True)
    appointment_1 = models.ForeignKey(Appointment, on_delete=CASCADE, related_name="appointment_1", null=True)
    appointment_2 = models.ForeignKey(Appointment, on_delete=CASCADE, related_name="appointment_2", null=True)
    date_confirmed = models.CharField(max_length=50, null=True, blank=True)
    reason = models.TextField(null=True)


class Symptom(models.Model):
    name = models.CharField(max_length=50)


class Prescription(models.Model):
    patient_first_name = models.CharField(_("patient first name"), max_length=150, null=True, blank=True)
    patient_last_name = models.CharField(_("patient last name"), max_length=150, null=True, blank=True)
    patient_address1 = models.CharField(max_length=200, null=True, blank=True)
    patient_address2 = models.CharField(max_length=200, null=True, blank=True)
    patient_city = models.CharField(max_length=20, null=True, blank=True)
    patient_state = models.CharField(max_length=30, null=True, blank=True)
    patient_zip = models.CharField(max_length=10, null=True, blank=True)
    patient_phone_number = models.CharField(max_length=50, null=True, blank=True)
    patient_fax_number = models.CharField(max_length=50, null=True, blank=True)
    patient_ssn = models.CharField(max_length=50, null=True, blank=True)
    medication = models.CharField(max_length=100, null=True, blank=True)
    dispensing_allowed = models.CharField(max_length=50, null=True, blank=True)
    substitute_allowed = models.BooleanField(default=False)
    quantity = models.CharField(max_length=50, null=True, blank=True)
    dosage_directions = models.CharField(max_length=100, null=True, blank=True)
    notes = models.CharField(max_length=100, null=True, blank=True)
    prescriber_state_license_number = models.CharField(
        max_length=50, null=True, blank=True
    )
    prescriber_address1 = models.CharField(max_length=200, null=True, blank=True)
    prescriber_address2 = models.CharField(max_length=200, null=True, blank=True)
    prescriber_city = models.CharField(max_length=20, null=True, blank=True)
    prescriber_state = models.CharField(max_length=30, null=True, blank=True)
    prescriber_zip = models.CharField(max_length=10, null=True, blank=True)
    prescriber_phone_number = models.CharField(max_length=50, null=True, blank=True)
    prescriber_fax_number = models.CharField(max_length=50, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

# class Profile(models.Model):
#         user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
#         # image = ImageField(default='default.jpg', upload_to='profile_pics', null=True)
#         # title = models.ForeignKey(User, related_name='type', on_delete=models.DO_NOTHING, null=True)
#         # email = models.ForeignKey(User, related_name='email', on_delete=models.DO_NOTHING, null=True)
#         # first_name = models.ForeignKey(User, related_name='first_name', on_delete=models.DO_NOTHING, null=True)
#         # last_name = models.ForeignKey(User, related_name='last_name', on_delete=models.DO_NOTHING, null=True)
# # related_name=""
#         def __str__(self):
#             return f'{self.user.first_name} {self.user.last_name} Profile'

class AnnotatedResponse(models.Model):
    uploaded_by = models.ForeignKey(Doctor, null=True, on_delete=DO_NOTHING, related_name='uploaded_by')
    shared_with_doctors = models.ManyToManyField('Doctor', blank=True)
    type = models.CharField(max_length=20, choices=UserType.choices, default="Doctor")
    shared_with = models.ForeignKey(Patient, null=True, on_delete=DO_NOTHING)
    file_type = models.CharField(max_length=100, null=True)
    file_subject = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to='doctors/annotatedResponses', null=True)
    shared_with_telepsycrx = models.BooleanField(default=False)

class CommunityResource(models.Model):
    uploaded_by = models.ForeignKey(Doctor, null=True, on_delete=DO_NOTHING)
    type = models.CharField(max_length=20, choices=UserType.choices, default="Doctor")
    shared_with = models.ForeignKey(Patient, null=True, blank=True, on_delete=DO_NOTHING)
    file_type = models.CharField(max_length=100, null=True)
    file_subject = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to='doctors/resources', null=True)

    # @property
    # def key(self):
    #     obj = FileSerializer.save()
    #     # for the sake of simplicity; assuming that all files have the format <name>.<ext>. Files without extension would error here.
    #     return str(obj.id) + '-' + FileSerializer.data['name'].split('.')[0] + '/' + FileSerializer.data['name']


class LockedResource(models.Model):
    uploaded_by = models.ForeignKey(Patient, null=True, on_delete=DO_NOTHING)
    type = models.CharField(max_length=20, choices=UserType.choices, default="Patient")
    shared_with = models.ForeignKey(Doctor, null=True, on_delete=DO_NOTHING)
    file_type = models.CharField(max_length=100, null=True)
    file_subject = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to='patient/resource_response', null=True)
    shared_with_telepsycrx = models.BooleanField(default=False)

    # @property
    # def key(self):
    #     obj = FileSerializer.save()
    #     # for the sake of simplicity; assuming that all files have the format <name>.<ext>. Files without extension would error here.
    #     return str(obj.id) + '-' + FileSerializer.data['name'].split('.')[0] + '/' + FileSerializer.data['name']


class TelepsycrxUpload(models.Model):
    uploaded_by = models.ForeignKey(User, null=True, on_delete=DO_NOTHING)
    type = models.CharField(max_length=20, choices=UserType.choices, default="Patient")
    file_type = models.CharField(max_length=100, null=True)
    file_subject = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to='telepsycrx', null=True)

class TelepsycrxDownload(models.Model):
    shared_with_patients = models.ManyToManyField('Patient', blank=True)
    shared_with_doctors = models.ManyToManyField('Doctor', blank=True)
    type = models.CharField(max_length=20, choices=UserType.choices, default="Patient")
    file_type = models.CharField(max_length=100, null=True)
    file_subject = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to='telepsycrx/neededDocs', null=True)

# class PatientUpload(models.Model):
#     uploaded_by = models.ForeignKey(Patient, null=True, on_delete=DO_NOTHING)
#     type = models.CharField(max_length=20, choices=UserType.choices, default="Patient")
#     file_type = models.CharField(max_length=10, null=True)
#     file_subject = models.CharField(max_length=100, null=True)
#     file = models.FileField(upload_to='patient/uploads', null=True)

    # @property
    # def key(self):
    #     obj = FileSerializer.save()
    #     # for the sake of simplicity; assuming that all files have the format <name>.<ext>. Files without extension would error here.
    #     return str(obj.id) + '-' + FileSerializer.data['name'].split('.')[0] + '/' + FileSerializer.data['name']


class RequestStatus:
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'
    CANCELLED = 'Cancelled'
    CHOICES = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (CANCELLED, 'Cancelled'),
    )


class ConsultRequest(models.Model):
    requester = models.ForeignKey(Patient, null=True, on_delete=DO_NOTHING)
    sent_to = models.ForeignKey('Doctor', null=True, on_delete=DO_NOTHING, related_name='consulted_to')
    specialty = models.CharField(max_length=150, null=True)
    is_accepted = models.BooleanField(default=False, null=True)
    is_referred = models.BooleanField(default=False, null=True)
    status = models.CharField(max_length=20, choices=RequestStatus.CHOICES, default=RequestStatus.PENDING)
    patient_full_name = models.CharField(max_length=200, null=True)
    patient_email = models.CharField(max_length=100, null=True)
    reason_for_request = models.CharField(max_length=150, null=True)
    details = models.TextField(null=True)
    requested_date = models.DateField(null=True)
    requested_time = models.TimeField(null=True)
    appointment_for = models.CharField(max_length=100, null=True)


class ReferralRequest(models.Model):
    sender = models.ForeignKey(User, null=True, on_delete=DO_NOTHING)
    doctors = models.ManyToManyField("Doctor", related_name="referred_to", through='ReferralRequestResponse')
    requested_specialty = models.CharField(max_length=150, null=True)
    chosen_specialty = models.CharField(max_length=150, null=True)
    reason_for_request = models.CharField(max_length=150, null=True)
    appointment_for = models.CharField(max_length=100, null=True)
    patient = models.ForeignKey(Patient, null=True, on_delete=DO_NOTHING)
    details = models.TextField(null=True)
    status = models.CharField(max_length=20, choices=RequestStatus.CHOICES, default=RequestStatus.PENDING)
    requested_date = models.DateField(null=True)
    requested_time = models.TimeField(null=True)
    outside_provider_invited = models.BooleanField(default=False, null=True)
    outside_provider_email = ArrayField(
        models.CharField(max_length=50), blank=True, default=list
    )

# {
#     "sender_id": 23,
#     "patient_id": 2,
#     "doctors_id": [3],
#     "requested_specialty": "Adult Psychiatry",
#     "chosen_specialty": "Psychiatry",
#     "details": "Referral from rest-framework",
#     "status": "Pending",
#     "requested_date": "2022-04-28",
#     "requested_time":"15:00:00",
#     "outside_provider_invited": "false",
#     "outside_provider_email": []
# }

class AppointmentConfirmation(models.Model):
    appointment_type = models.CharField(max_length=50, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(null=True)
    pharmacy = models.ForeignKey(
        Pharmacy, null=True, on_delete=models.SET_NULL, default="FakePharm"
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)


class ReferralRequestResponse(models.Model):
    referral = models.ForeignKey(ReferralRequest, null=True, on_delete=DO_NOTHING)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=DO_NOTHING)
    status = models.CharField(max_length=20, choices=RequestStatus.CHOICES, default=RequestStatus.PENDING)

