import requests

from django.urls import reverse
from test_plus import APITestCase, TestCase

from rest_framework.test import force_authenticate, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from core.tests import CoreTestCase

from ..choices import UserType
from ..factories import DoctorFactory, PatientFactory, UserFactory
from ..models import Patient, Doctor, Appointment, Relationship


class TestDoctorViews(APITestCase):
    def make_doctor_user(self, doctor=None):
        return UserFactory(type=UserType.DOCTOR)

    def setUp(self):
        self.doctor = DoctorFactory()
        # associate the user with the doctor
        self.doctor_user = self.make_doctor_user()

        self.api_client = APIClient()
        self.api_client.credentials(
            HTTP_AUTHORIZATION=f"JWT {RefreshToken.for_user(self.doctor_user).access_token}"
        )

    def test_doctors_me_smoke(self):
        url = reverse("accounts:doctors-me")
        response = self.get(url)
        self.assertEqual(response.status_code, 401)

        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_doctors_me_scope(self):
        # ensure that the right user type is able to access this endpoint (doctor vs. patient)
        self.skipTest("")

    def test_doctors_patients_smoke(self):
        url = reverse("accounts:doctors-patients", kwargs=dict(pk=self.doctor.pk))
        response = self.get(url)
        self.assertEqual(response.status_code, 401)

        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_doctors_patients_scope(self):
        # ensure that the right user type is able to access this endpoint (doctor vs. patient)
        # ensure that the user calling for this data is actually the doctor themselves
        self.skipTest("")

    def test_doctors_slots_smoke(self):
        url = reverse("accounts:doctors-slots", kwargs=dict(pk=self.doctor.pk))
        response = self.get(url)
        self.assertEqual(response.status_code, 401)

        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_doctors_slots_scope(self):
        # ensure that the right user type is able to access this endpoint (doctor vs. patient)
        # ensure that the user calling for this data is actually the doctor themselves
        self.skipTest("")

    def test_doctors_accepting_smoke(self):
        url = reverse("accounts:doctors-accepting")
        response = self.get(url)
        self.assertEqual(response.status_code, 401)

        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 200)


class TestPatientViews(APITestCase):
    def make_patient_user(self, patient=None):
        user = UserFactory(type=UserType.PATIENT)
        if patient:
            _ = Relationship.objects.create(user=user, patient=patient)
        return user

    def setUp(self):
        self.patient = PatientFactory()
        # associate the user with the doctor
        self.patient_user = self.make_patient_user(patient=self.patient)

        self.api_client = APIClient()
        self.api_client.credentials(
            HTTP_AUTHORIZATION=f"JWT {RefreshToken.for_user(self.patient_user).access_token}"
        )

    def test_patients_me_smoke(self):
        url = reverse("accounts:patients-me")
        response = self.get(url)
        self.assertEqual(response.status_code, 401)

        self.skipTest("skipping because this view is not functional")
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_patients_me_scope(self):
        # ensure that patients are the ones calling this
        self.skipTest("")

    def test_patients_pdf_smoke(self):
        url = reverse("accounts:patients-pdf", kwargs=dict(pk=self.patient.pk))
        response = self.get(url)
        self.assertEqual(response.status_code, 401)

        self.skipTest(
            "should test a successful response, but out of scope for this project because of PDF handling concerns"
        )
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 200)


class TestUserViews(APITestCase):
    def make_patient_user(self, patient=None, doctor=None):
        user = UserFactory(type=UserType.PATIENT)

        if patient:
            _ = Relationship.objects.create(user=user, patient=patient)

        if doctor:
            user.doctors.add(doctor)

        return user

    def make_doctor_user(self, patient=None, doctor=None):
        # TODO: associate the user with the Doctor
        return UserFactory(type=UserType.DOCTOR)

    def setUp(self):
        self.patient = PatientFactory()
        self.doctor = DoctorFactory()
        self.patient_user = self.make_patient_user(
            patient=self.patient, doctor=self.doctor
        )
        self.doctor_user = self.make_doctor_user(doctor=self.doctor)

        self.api_client = APIClient()
        self.api_client.credentials(
            HTTP_AUTHORIZATION=f"JWT {RefreshToken.for_user(self.patient_user).access_token}"
        )

    def test_user_doctor_colleagues_smoke(self):
        self.skipTest("view not functional")
        url = reverse(
            "accounts:users-colleagues",
            kwargs=dict(pk=self.patient_user.pk),
        )
        response = self.get(url)
        self.assertEqual(response.status_code, 401)

        # self.skipTest("skipping because this view is not functional")
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_journals_by_doctor_smoke(self):
        url = reverse(
            "accounts:users-journals",
            kwargs=dict(pk=self.patient_user.pk),
        )
        response = self.get(url)
        self.assertEqual(response.status_code, 401)

        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_patients_me_scope(self):
        # ensure the right user role is calling this
        self.skipTest("")

    def test_user_doctors_smoke(self):
        url = reverse(
            "accounts:users-doctors",
            kwargs=dict(pk=self.patient_user.pk),
        )
        response = self.get(url)
        self.assertEqual(response.status_code, 401)

        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_doctors_scope(self):
        # ensure the right user role is calling this
        self.skipTest("")

    def test_user_patients_smoke(self):
        url = reverse(
            "accounts:users-patients",
            kwargs=dict(pk=self.doctor_user.pk),
        )
        response = self.get(url)
        self.assertEqual(response.status_code, 401)

        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_patients_scope(self):
        # ensure the right user role is calling this
        self.skipTest("")

    def test_user_me_smoke(self):
        url = reverse(
            "accounts:users-me",
            kwargs=dict(pk=self.doctor_user.pk),
        )
        response = self.get(url)
        self.assertEqual(response.status_code, 401)

        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_validate_email_smoke(self):
        url = reverse(
            "accounts:users-validate_email",
        )
        response = self.post(url)
        # should return 400 for invalid body rather than 401 due to lack of auth
        self.assertEqual(response.status_code, 400)

    def test_user_validate_phone_smoke(self):
        url = reverse(
            "accounts:users-validate_phone",
            kwargs=dict(pk=self.doctor_user.pk),
        )
        response = self.post(url)
        self.assertEqual(response.status_code, 200)

    def test_user_complete_password_reset_smoke(self):
        url = reverse(
            "accounts:users-complete_password_reset",
        )
        response = self.post(url)
        # should return 400 for invalid body rather than 401 due to lack of auth
        self.assertEqual(response.status_code, 400)

    def test_user_request_password_reset_smoke(self):
        url = reverse(
            "accounts:users-request_password_reset",
        )
        response = self.post(url)
        # should return 400 for invalid body rather than 401 due to lack of auth
        self.assertEqual(response.status_code, 400)

    # @action(methods=["post"], detail=False)
    # def request_password_reset(self, request):
    #     email = request.data.get("email")
    #     user = User.objects.filter(email=email).first()
    #     if user:
    #         user.send_password_reset_token()

    #     return Response()
