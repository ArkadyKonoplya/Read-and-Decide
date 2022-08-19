import arrow
import factory

from factory import fuzzy
from faker import Faker
from random import randint

from .choices import AppointmentStatus, TITLES, Gender, UserType
from .models import Appointment, Doctor, Patient, User

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("ascii_email")
    type = fake.random_element(elements=[val for val, _ in UserType.choices])
    phone_number = factory.Faker("phone_number")
    # doctors = models.ManyToManyField("Doctor", blank=True)
    # patients = models.ManyToManyField("Patient", blank=True)
    is_active = True


class DoctorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Doctor

    is_approved = True
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    title = fake.random_element(elements=[title for title, _ in TITLES])
    email = factory.Faker("ascii_email")
    phone_number = factory.Faker("phone_number")
    fax_number = factory.Faker("phone_number")
    address1 = factory.Faker("street_address")
    city = factory.Faker("city")
    # coordinates with default timezone of Honolulu
    state = "HI"
    zip = factory.Faker("postcode")


class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Patient

    email = factory.Faker("ascii_email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone_number = factory.Faker("phone_number")
    date_of_birth = arrow.get("1950-01-01").date()
    gender = fake.random_element(elements=[val for val, _ in Gender.choices])
    address1 = factory.Faker("street_address")
    city = factory.Faker("city")
    state = "HI"
    zip = factory.Faker("postcode")


class AppointmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Appointment

    date = arrow.utcnow().shift(days=7).datetime
    doctor = factory.SubFactory(DoctorFactory)
    status = AppointmentStatus.CONFIRMED
    # TODO: handle me
    # requested_by = models.ForeignKey(User, on_delete=PROTECT, null=True)
