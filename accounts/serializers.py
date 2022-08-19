from dataclasses import fields
from email.mime import image
from django.contrib.auth import password_validation
from pkg_resources import require
from rest_framework.fields import URLField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField
# from accounts.s3 import S3

from .choices import RelationshipType
from .fields import PhoneNumberField, DateTimeField
from .models import (
    User,
    Patient,
    Invitation,
    Relationship,
    Doctor,
    InsurancePlan,
    Pharmacy,
    Appointment,
    Symptom,
    Prescription,
    AppointmentConfirmation,
    ReferralRequest,
    ReferralRequestResponse,
    ConsultRequest,
    LockedResource,
    CommunityResource,
    TelepsycrxUpload,
    AnnotatedResponse,
    TelepsycrxDownload, RescheduleAppointment,
    # PatientUpload,
)

# customzing what gets returned on logging in
# (obtaining the JWT)

class PictureSerialiser(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = User
        fields = ('field', 'image', 'image_url')

    def get_image_url(self, obj):
        return obj.image.url

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super().validate(attrs)

        
    # image_url = serializers.SerializerMethodField('get_image_url')
    # class Meta:
    #     model = User
    #     fields = ['image']

    #     def get_image_url(self, obj):
    #         return obj.image.url

        # Email has to be unique, and their has to be a doctor with the
        # same email, first name, and last name
        # Can also be done at registration
        if self.user.type == "Doctor":
            # image = User.objects.filter(image=self.user.image)
            doctor_object = Doctor.objects.filter(email=self.user.email)
            id = doctor_object.first().pk
            title = doctor_object.get(pk=id).title
            is_approved = doctor_object.get(pk=id).is_approved
            is_partner_account = doctor_object.get(pk=id).is_partner_account
            data.update({
                "doctor_id": id, 
                "doctor_title": title, 
                "is_approved": is_approved, 
                "is_partner_account": is_partner_account})

        if self.user.type == "Patient":
            image = User.objects.filter(image=self.user.image)
            patient_object = Patient.objects.filter(email=self.user.email)
            id = patient_object.first().pk
            is_subscribed = patient_object.first().is_subscribed
            subscription_type = patient_object.first().subscription_type
            is_identified = patient_object.first().is_identified
            data.update({
                "patient_id": id, 
                "is_subscribed": is_subscribed,
                "subscription_type": subscription_type,
                "is_identified": is_identified
                
                })

        # Custom data you want to include
        data.update({
            'type': self.user.type,
            'id': self.user.id,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'image': self.user.image.url
        })

        return data

    # @classmethod
    # def get_token(cls, user):
    #     token = super(MyTokenObtainPairSerializer, cls).get_token(user)

    #     # Add custom claims
    #     token['type'] = user.type
    #     token['id'] = user.id
    #     return token


class DoctorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    phone_number = PhoneNumberField(read_only=True)
    timezone = TimeZoneSerializerField()
    url = serializers.HyperlinkedIdentityField(view_name="accounts:doctor-detail")
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        user = User.objects.get(email=obj.email)
        return user.image.url

    class Meta:
        model = Doctor
        # fields = '__all__'
        fields = [
            "url",
            "image",
            "about",
            "address1",
            "address2",
            "board_certified_speciality",
            "city",
            "dea",
            "email",
            "fax_number",
            "first_name",
            "fri_end",
            "fri_off",
            "fri_start",
            "id",
            "is_approved",
            "last_name",
            "mon_end",
            "mon_off",
            "mon_start",
            "npi",
            "phone_number",
            "sat_end",
            "sat_off",
            "sat_start",
            "since",
            "state",
            "state_license_numbers",
            "states",
            "sun_end",
            "sun_off",
            "sun_start",
            "thu_end",
            "thu_off",
            "thu_start",
            "timezone",
            "title",
            "tue_end",
            "tue_off",
            "tue_start",
            "wed_end",
            "wed_off",
            "wed_start",
            "zip",
            "journal_entries_for_provider",
        ]
        depth = 1  # Will be able to access foreign keys


class PatientSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()
    url = serializers.HyperlinkedIdentityField(view_name="accounts:patient-detail")
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        user = User.objects.get(email=obj.email)
        return user.image.url

    class Meta:
        model = Patient
       
        fields = [
            'url', 'image', 'id', 'email', 'first_name', 'last_name', 'is_subscribed', 'subscription_type',
            'phone_number', 'date_of_birth', 'height', 'height_ft', 'height_inch', 'provider_patient_notes', 'gender', 'address1','address2','city', 'state', 'zip', 'insurance_plan_username', 'pharmacy_plan','pharmacy_member', 'pharmacy_bin', 'freemium_doc_array',
            'weight','medications','allergies','smoke','alcohol','asthma','kidney_problems','high_blood_pressure','low_blood_pressure','diabetes','heart_problems','headaches','urinary_tract_infections',
            'depression','seizures','stroke','thyroid_disease','arrhythmias','anxiety','panic_attacks','copd','eczema','psoriasis','cancer','other_problems','family_asthma','family_stroke','family_diabetes','family_heart_problems','family_high_blood_pressure',
            'family_low_blood_pressure','family_thyroid_disease','family_arrhythmias','family_anxiety', 'family_panic_attacks', 'family_copd', 'family_eczema', 'family_psoriasis', 'family_headaches', 
            'family_seizures', 'family_depression', 'family_depression', 'family_kidney_problems', 'family_urinary_tract_infections', 'family_cancer', 'family_other_problems'
            ]
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(required=False)
    doctors = DoctorSerializer(many=True, read_only=True)
    patients = PatientSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="accounts:user-detail")


    # fields = ['image']

    class Meta:
        model = User
        fields = [
            "url",
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "type",
            "image",
            "provider_notes",
            "journal_entries",
            "doctors",
            "patients",
        ]
        depth = 1
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value


class PatientListSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()

    class Meta:
        model = Patient
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "date_of_birth",
            "height",
        ]


class InvitationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Invitation
        fields = "__all__"

    def get_user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"


class RelationshipSerializer(serializers.ModelSerializer):
    patient = PatientListSerializer()

    class Meta:
        model = Relationship
        fields = ["id", "relationship", "patient"]


class RelationshipCreationSerializer(serializers.ModelSerializer):
    relationship = serializers.ChoiceField(choices=RelationshipType.choices)

    class Meta:
        model = Patient
        exclude = (
            "email",
            "phone_number",
        )


# class DoctorSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(read_only=True)
#     phone_number = PhoneNumberField(read_only=True)
#     timezone = TimeZoneSerializerField()

#     class Meta:
#         model = Doctor
#         fields = '__all__'
#         depth = 1 # Will be able to access foreign keys


class DoctorListSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()

    class Meta:
        model = Doctor
        fields = ["id", "title", "first_name", "last_name", "phone_number"]


class InsurancePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsurancePlan
        fields = "__all__"


class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    patient_id = serializers.IntegerField(write_only=True)
    doctor = DoctorListSerializer(read_only=True)
    doctor_id = serializers.IntegerField(write_only=True)
    date = serializers.CharField()

    class Meta:
        model = Appointment
        fields = "__all__"


class AppointmentListSerializer(serializers.ModelSerializer):
    patient = PatientListSerializer()
    doctor = DoctorListSerializer()
    requested_by = UserSerializer()
    date = serializers.CharField()

    class Meta:
        model = Appointment
        exclude = ["questionnaires"]

    def get_patient(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"

    def get_doctor(self, obj):
        return f"{obj.doctor.title}. {obj.doctor.first_name} {obj.doctor.last_name}"


class RescheduleAppointmentSerializer(serializers.ModelSerializer):
    appointment_ref = AppointmentSerializer(read_only=True)
    appointment_ref_id = serializers.IntegerField(write_only=True)
    appointment_1 = AppointmentSerializer()
    appointment_2 = AppointmentSerializer()

    class Meta:
        model = RescheduleAppointment
        fields = [
            "id",
            "appointment_ref",
            "appointment_ref_id",
            "appointment_1",
            "appointment_2",
            "date_confirmed",
            "reason"
        ]


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = "__all__"


class PrescriptionSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    doctor_id = serializers.IntegerField(write_only=True)
    patient_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Prescription
        fields = "__all__"


class AppointmentConfirmationSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    doctor_id = serializers.IntegerField(write_only=True)
    patient_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = AppointmentConfirmation
        fields = "__all__"


# TODO: Add user image, type, and name to the serializer
class ConsultRequestSerializer(serializers.ModelSerializer):
    requester = PatientSerializer(read_only=True)
    requester_id = serializers.IntegerField(write_only=True)
    # patient_object = PatientSerializer(read_only=True)
    sent_to = DoctorSerializer(read_only=True)
    sent_to_id = serializers.IntegerField(write_only=True)
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        user = User.objects.get(email=obj.requester.email)
        return user.image.url

    class Meta:
        model = ConsultRequest
        fields = '__all__'


class AppointmentConfirmationSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    doctor_id = serializers.IntegerField(write_only=True)
    patient_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = AppointmentConfirmation
        fields = '__all__'


class ReferralRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sender_id = serializers.IntegerField(write_only=True)
    patient = PatientSerializer(read_only=True)
    patient_id = serializers.IntegerField(write_only=True)
    doctors = DoctorSerializer(many=True, read_only=True)
    doctors_id = serializers.ListField(write_only=True)

    def create(self, validated_data):
        doctors_id = validated_data.pop('doctors_id')
        referral = ReferralRequest.objects.create(**validated_data)
        for doctor_id in doctors_id:
            ReferralRequestResponse.objects.create(referral=referral, doctor_id=doctor_id)
        return referral

    class Meta:
        model = ReferralRequest
        fields = '__all__'


class ReferralRequestResponseSerializer(serializers.ModelSerializer):
    referral = ReferralRequestSerializer(read_only=True)
    referral_id = serializers.IntegerField(write_only=True)
    doctor = PatientSerializer(read_only=True)
    doctor_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ReferralRequestResponse
        fields = '__all__'


# class FileSerializer(serializers.ModelSerializer):
#     file_url = serializers.SerializerMethodField()

#     class Meta:
#         model = LockedResource, CommunityResource, User, TelepsycrxUpload
#         fields = 'file', 'license_pdf_upload', 'image'

#     def get_file_url(self, obj):
#         return S3().get_file(obj.key)


class LockedResourceSerializer(serializers.ModelSerializer):
    uploaded_by = PatientSerializer(read_only=True)
    uploaded_by_id = serializers.IntegerField(write_only=True)
    shared_with = DoctorSerializer(read_only=True)
    shared_with_id = serializers.IntegerField(write_only=True, required=False)
    uploaded_by_name = serializers.SerializerMethodField()
    uploaded_by_image = serializers.SerializerMethodField()

    def get_uploaded_by_name(self, obj):
        email = obj.uploaded_by.email
        user = User.objects.get(email=email)
        return user.first_name + " " + user.last_name

    def get_uploaded_by_image(self, obj):
        email = obj.uploaded_by.email
        user = User.objects.get(email=email)
        return user.image.url

    class Meta:
        model = LockedResource
        fields = '__all__'

class CommunityResourceSerializer(serializers.ModelSerializer):
    uploaded_by = DoctorSerializer(read_only=True)
    uploaded_by_id = serializers.IntegerField(write_only=True)
    shared_with = PatientSerializer(read_only=True)
    shared_with_id = serializers.IntegerField(write_only=True, required=False)
    uploaded_by_name = serializers.SerializerMethodField()
    uploaded_by_image = serializers.SerializerMethodField()

    def get_uploaded_by_name(self, obj):
        email = obj.uploaded_by.email
        user = User.objects.get(email=email)
        return user.first_name + " " + user.last_name

    def get_uploaded_by_image(self, obj):
        email = obj.uploaded_by.email
        user = User.objects.get(email=email)
        return user.image.url

    class Meta:
        model = CommunityResource
        fields = '__all__'

class TelepsycrxUploadSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    uploaded_by_id = serializers.IntegerField(write_only=True)
    uploaded_by_name = serializers.SerializerMethodField()
    uploaded_by_image = serializers.SerializerMethodField()

    def get_uploaded_by_name(self, obj):
        user = obj.uploaded_by
        return user.first_name + " " + user.last_name

    def get_uploaded_by_image(self, obj):
        user = obj.uploaded_by
        return user.image.url

    class Meta:
        model = TelepsycrxUpload
        fields = '__all__'

class TelepsycrxDownloadSerializer(serializers.ModelSerializer):
    shared_with_patients = PatientSerializer(many=True, read_only=True)
    shared_with_patients_id = serializers.ListField(write_only=True, required=False)
    shared_with_doctors = DoctorSerializer(many=True, read_only=True)
    shared_with_doctors_id = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = TelepsycrxDownload
        fields = '__all__'

class AnnotatedResponseSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    uploaded_by_id = serializers.IntegerField(write_only=True)
    shared_with = PatientSerializer(read_only=True)
    shared_with_id = serializers.IntegerField(write_only=True, required=False)
    shared_with_doctors = DoctorSerializer(read_only=True, many=True)
    shared_with_doctors_id = serializers.ListField(write_only=True, required=False)
    uploaded_by_name = serializers.SerializerMethodField()
    uploaded_by_image = serializers.SerializerMethodField()

    def get_uploaded_by_name(self, obj):
        email = obj.uploaded_by.email
        user = User.objects.get(email=email)
        return user.first_name + " " + user.last_name

    def get_uploaded_by_image(self, obj):
        email = obj.uploaded_by.email
        user = User.objects.get(email=email)
        return user.image.url

    class Meta:
        model = AnnotatedResponse
        fields = '__all__'
