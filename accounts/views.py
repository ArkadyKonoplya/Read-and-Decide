import datetime

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from hashids import Hashids
from rest_framework import viewsets, status, permissions, parsers, serializers
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
# from twilio.base.exceptions import TwilioRestException
import botocore
import arrow
# from twilio.jwt.access_token import AccessToken
# from twilio.jwt.access_token.grants import VideoGrant
from django_filters.rest_framework import DjangoFilterBackend
from django_renderpdf.helpers import render_pdf

from django.http import JsonResponse
from django.forms.models import model_to_dict

#timezone
from django.shortcuts import redirect, render

from .filters import (
    StateFilterBackend, AcceptingFilterBackend,
)

from .serializers import (
    AppointmentListSerializer,
    AppointmentSerializer,
    CommunityResourceSerializer,
    DoctorSerializer,
    InsurancePlanSerializer,
    InvitationSerializer,
    MyTokenObtainPairSerializer,
    PatientSerializer,
    PharmacySerializer,
    PrescriptionSerializer,
    RelationshipCreationSerializer,
    RelationshipSerializer,
    SymptomSerializer,
    TelepsycrxUploadSerializer,
    UserSerializer,
    AppointmentConfirmationSerializer,
    ConsultRequestSerializer,
    # FileSerializer,
    LockedResourceSerializer,
    CommunityResourceSerializer,
    TelepsycrxUploadSerializer,
    TelepsycrxDownloadSerializer,
    ReferralRequestSerializer,
    ReferralRequestResponseSerializer,
    AnnotatedResponseSerializer,
    RescheduleAppointmentSerializer,
)
from .models import (
    Appointment,
    Doctor,
    InsurancePlan,
    Invitation,
    Patient,
    Pharmacy,
    Prescription,
    Relationship,
    Symptom,
    User,
    AppointmentConfirmation,
    ConsultRequest,
    ReferralRequest,
    ReferralRequestResponse,
    LockedResource,
    CommunityResource,
    TelepsycrxUpload,
    AnnotatedResponse,
    TelepsycrxDownload, RescheduleAppointment, RequestStatus,
)

hashids = Hashids(min_length=8)

# class FileView(APIView):
#     # @action(methods=['post'], detail=False)
#     def post(self, request):
#         serializer = FileSerializer(data={'name': request.data['name'], 'ext': request.data['name'].split('.')[1]})
#         serializer.is_valid(raise_exception=True)
#         obj = serializer.save()

#         url = S3().get_presigned_url(obj.key)
#         return Response({'url': url, 'id': id})
    
class LockedResourceViewset(viewsets.ModelViewSet):
    queryset = LockedResource.objects.all()
    serializer_class = LockedResourceSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.type == 'Doctor':
            doctor = Doctor.objects.get(email=request.user.email)
            queryset = self.get_queryset().filter(shared_with=doctor.id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        elif request.user.type == 'Patient':
            patient = Patient.objects.get(email=request.user.email)
            queryset = self.get_queryset().filter(uploaded_by=request.user.id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CommunityResourceViewset(viewsets.ModelViewSet):
    queryset = CommunityResource.objects.all()
    serializer_class = CommunityResourceSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.type == 'Patient':
            patient = Patient.objects.get(email=request.user.email)
            queryset = self.get_queryset().filter(shared_with=patient.id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        elif request.user.type == 'Doctor':
            doctor = Doctor.objects.get(email=request.user.email)
            queryset = self.get_queryset().filter(uploaded_by=doctor.id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class TelepsycrxUploadViewset(viewsets.ModelViewSet):
    queryset = TelepsycrxUpload.objects.all()
    serializer_class = TelepsycrxUploadSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(uploaded_by=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class TelepsycrxDownloadViewset(viewsets.ModelViewSet):
    queryset = TelepsycrxDownload.objects.all()
    serializer_class = TelepsycrxDownloadSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.type == 'Doctor':
            doctor = Doctor.objects.get(email=request.user.email)
            queryset = self.get_queryset().filter(shared_with_doctors=doctor.id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        elif request.user.type == 'Patient':
            patient = Patient.objects.get(email=request.user.email)
            queryset = self.get_queryset().filter(shared_with_patients=patient.id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class AnnotatedResponseViewset(viewsets.ModelViewSet):
    queryset = AnnotatedResponse.objects.all()
    serializer_class = AnnotatedResponseSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if request.user.type == 'Doctor':
            doctor = Doctor.objects.get(email=request.user.email)
            queryset = self.get_queryset().filter(uploaded_by=doctor.id)
            queryset |= self.get_queryset().filter(shared_with_doctors=doctor.id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        elif request.user.type == 'Patient':
            patient = Patient.objects.get(email=request.user.email)
            queryset = self.get_queryset().filter(shared_with=patient.id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

#  signing up a user with a custom view
class ObtainTokenPairViewWithUserType(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

#  signing up a user
class CustomUserCreate(APIView):
    reg_serializer = UserSerializer
    permission_classes = [permissions.AllowAny]

    

    def post(self, request, format='json'):
        print(request.data)
        data = request.data
        reg_serializer = UserSerializer(data=data)
        if reg_serializer.is_valid():
            password = reg_serializer.validated_data.get('password')
            reg_serializer.validated_data['password'] = make_password(password)
            new_user = reg_serializer.save()

            # If the user is a doctor, create a doctor object,
            # otherwise create a patient object
            # Now creating a doctor or patient object along with the user object
            if new_user.type == 'Doctor':
                user_model = Doctor
            elif new_user.type == 'Patient':
                user_model = Patient

            user_model.objects.create(email=new_user.email, first_name=new_user.first_name,
                                      last_name=new_user.last_name)
            data.update({'id': User.objects.get(email=new_user.email).pk})

            if new_user:
                return Response(data, status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlacklistTokenUpdateView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(methods=['get'], detail=True)
    def get_doctor_colleages(self, request, pk, *args, **kwargs):
        user = self.get_object()
        user_object_serializer = self.get_serializer(user)
        doctor_colleage_list = user_object_serializer.data.get('doctors')
        key_list = []
        value_list = []
        doctor_colleage_dictionary = {}
        
        for i in range(len(doctor_colleage_list)):
            colleage_data = []

            serialized_doctor_id = user_object_serializer.data.get('doctors')[i].get('id')
            key_list.append(serialized_doctor_id)
            colleage_doctor_object = user_object_serializer.data.get('doctors')[i].get('first_name', 'last_name','email')

            for i in range(len(colleage_doctor_object)):
                # I don't understand, this variable is defined already.
                print("Colleage_Object", colleage_doctor_object[i])

                # Only adds doctors that are NOT the current user's pk
                if colleage_doctor_object[i].get('id') is not user.pk:
                    colleage_data.append(colleage_doctor_object[i])
            value_list.append(colleage_data)
            print("Colleage List:", value_list)

            doctor_colleage_dictionary = dict(zip(key_list, value_list))
        return Response(doctor_colleage_dictionary)


    @action(methods=['get'], detail=True)
    def get_personal_journals_by_doctor(self, request, pk, *args, **kwargs):
        user = self.get_object()
        user_object_serializer = self.get_serializer(user)
        user_doctors_list = user_object_serializer.data.get('doctors')
        key_list = []
        value_list = []

        doctor_journal_entry_dictionary = {}

        # Create dictionary - key: patient email, value: doctors with journal entries
        for i in range(len(user_doctors_list)):
            same_author_entries_list = []
            serialized_doctor_email = user_object_serializer.data.get('doctors')[i].get('email')

            key_list.append(serialized_doctor_email)
            journal_entries_list = user_object_serializer.data.get('doctors')[i].get('journal_entries_for_provider')

            for i in range(len(journal_entries_list)):
                print(journal_entries_list[i])

                # Only adds journal written by the user calling this method
                if journal_entries_list[i].get('author') is user.pk:
                    same_author_entries_list.append(journal_entries_list[i])
            value_list.append(same_author_entries_list)
            print("VALUE LIST", value_list)

            doctor_journal_entry_dictionary = dict(zip(key_list, value_list))
        return Response(doctor_journal_entry_dictionary)

    @action(methods=['get'], detail=True)
    def get_user_doctors(self, request, pk):
        '''
        This method returns all the doctors associated
        with a user only with info that is necessary
        for the user to see.
        '''
        user = self.get_object()
        user_doctors_list = user.doctors.all()
        doctors_dictionary = {}
        key_list = []
        value_list = []
        print(user_doctors_list)
        for doctor in user_doctors_list:
            key_list.append(doctor.pk)

            # Only get doctors required information:
            doctor_info_dictionary = {
                "first_name": doctor.first_name,
                "last_name": doctor.last_name,
                "email": doctor.email,  
                "id": doctor.pk
            }
            value_list.append(doctor_info_dictionary)
            doctors_dictionary = dict(zip(key_list, value_list)) 

        return Response(doctors_dictionary)

    @action(methods=['get'], detail=True)
    def get_doctor_patients(self, request, pk, *args, **kwargs):
        # Optimize this from user serializer
        user = self.get_object()
        archived = request.query_params.get('archived', False)
        patients_list = user.patients.all()
        print(patients_list)
        patients_dictionary = {}
        key_list = []
        value_list = []

        # Create dictionary - key: patient email, value: patient object
        for patient in patients_list:
            patient_object = Patient.objects.get(email=patient.email)
            serialized_patient_object = PatientSerializer(patient_object, many=False, context={'request': None})
            patient_email = patient_object.email
            key_list.append(patient_email)
            if archived:
                value_list.append(serialized_patient_object.data)
            else:
                for note in serialized_patient_object.data.get('provider_patient_notes'):
                    # Check for archived notes and remove them from the list
                    if note.get('archived') is True:
                        print(serialized_patient_object.data.get('provider_patient_notes')[0])
                        del serialized_patient_object.data.get('provider_patient_notes')[0]

                value_list.append(serialized_patient_object.data)
            patients_dictionary = dict(zip(key_list, value_list))
            print(patients_dictionary)
        return Response(patients_dictionary)

    @action(methods=['post'], detail=True)
    def resend(self, request, pk=None):
        user = self.get_object()
        user.send_activation_token()
        return Response()

    @action(methods=['get'], detail=True)
    def me(self, request, pk=None):
        user = self.get_object()
        # Assumes the user is authenticated, handle this according your needs
        # user_id = request.user.id
        return self.retrieve(request, user.id)

    @action(methods=['post'], detail=False)
    def validate_new_user(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        user = User.objects.get(email=email, activation_token=code)

        if user is None:
            return Response(data={
                'code': 'Invalid code',
            }, status=400)

        if user.activation_token != code:
            return Response(data={
                'code': 'Invalid code',
            }, status=400)

        if user.activation_expired < timezone.now():
            return Response(data={
                'code': 'Expired code',
            }, status=400)

        print(request.data.get('email'))
        print(request.data.get('code'))
        user.activation_expired = None
        user.is_active = True
        user.save(update_fields=['activation_token', 'activation_expired', 'is_active'])
        return Response('Your account has now been activated.',
                        status=status.HTTP_202_ACCEPTED)

    # Modified from previous developer
    @action(methods=['post'], detail=True)
    def validate_phone(self, request, pk=None):
        user: User = self.get_object()

        phone_number: str = request.data.get('phone_number')
        code: str = request.data.get('code')

        if not code:
            user.phone_number = phone_number
            user.save(update_fields=['phone_number'])
            try:
                user.send_phone_activation_token()
                return Response()
            # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/error-handling.html
            except botocore.exceptions.ClientError as e:
                # Possibly change this:
                msg = e.msg
                if ':' in msg:
                    msg = ':'.join(msg.split(':')[1:]).strip()

                return Response({
                    'phone_number': msg,
                }, status=status.HTTP_400_BAD_REQUEST)

        if user.phone_number != phone_number or user.phone_activation_token != str(code):
            return Response(data={
                'code': 'Invalid code',
            }, status=400)

        if user.phone_activation_expired < timezone.now():
            return Response(data={
                'code': 'Expired code',
            }, status=400)

        user.phone_activated = True
        user.phone_activation_token = None
        user.phone_activation_expired = None
        user.save(update_fields=['phone_activation_token', 'phone_activation_expired',
                                 'phone_activated'])
        return Response()

    # Code can be taken from the url like with confirming a user's email
    @action(methods=['post'], detail=False)
    def password_reset(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        print(f"{email}\n{code}")
        print(f"{user.password_reset_token} {code}")
        print(f"{password}")

        if not user or user.password_reset_token != str(code):
            return Response(data={
                'code': 'Invalid code',
            }, status=400)

        if user.password_reset_expired < timezone.now():
            return Response(data={
                'code': 'Expired code',
            }, status=400)

        if password:
            user.set_password(password)
            user.password_reset_token = None
            user.password_reset_expired = None
            user.save(update_fields=['password', 'password_reset_token', 'password_reset_expired'])

        return Response()

    @action(methods=['post'], detail=False)
    def request_password_reset(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            user.send_password_reset_token()

        return Response()


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False)
    def me(self, request):
        relationship = get_object_or_404(
            Relationship.objects, user=request.user, relationship='Me')
        return Response(PatientSerializer(relationship.patient).data)

    @action(methods=['get'], detail=True)
    def pdf(self, request, pk=None):
        patient = Patient.objects.get(id=pk)
        patient_serializer = PatientSerializer(patient, context={'request': request})

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(patient.first_name)

        context = {
            'request': request,
            'patient': patient_serializer.data,
        }

        render_pdf('patient_pdf.html', response, context=context)
        return response


class InvitationViewSet(viewsets.ModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer

    def get_queryset(self):
        return super().get_queryset().filter(Q(user=self.request.user) | Q(email=self.request.user.email))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['user'] = request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


def get_age(date_of_birth):
    today = timezone.now()
    date_of_birth = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d')
    return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))


class RelationshipViewSet(viewsets.ModelViewSet):
    queryset = Relationship.objects.select_related('patient')
    serializer_class = RelationshipSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return RelationshipCreationSerializer

        return RelationshipSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)

        user = request.user
        patient = Patient.objects.create(email=user.email,
                                         phone_number=user.phone_number,
                                         **serializer.validated_data)

        relationship = Relationship(
            user=user, relationship=serializer.data['relationship'])
        relationship.patient = patient
        relationship.save()

        return Response(RelationshipSerializer(relationship).data, status=status.HTTP_201_CREATED, headers=headers)


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filter_backends = [DjangoFilterBackend, StateFilterBackend, AcceptingFilterBackend]
    filterset_fields = ['board_certified_speciality', 'state', 'accepting_new_patients']
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False)
    def me(self, request):
        return Response(self.get_serializer(self.request.user.doctors.all(), many=True).data)

    @action(methods=['get'], detail=True)
    def patients(self, request, pk):
        doctor = self.get_object()
        patients = Patient.objects.filter(
            id__in=Appointment.objects.filter(doctor=doctor).values_list('patient', flat=True).distinct())
        return Response(PatientSerializer(patients, many=True).data)


    @action(methods=['get'], detail=True)
    def slots(self, request, pk):
        date = timezone.now().date()
        if request.query_params.get('date'):
            date = datetime.datetime.strptime(
                request.query_params.get('date'), '%Y-%m-%d').date()

        doctor = self.get_object()
        day = date.isoweekday() % 7 + 1

        from_ = datetime.datetime(
            date.year, date.month, date.day, 0, 0, 0, tzinfo=doctor.timezone)
        to = datetime.datetime(date.year, date.month,
                               date.day, 23, 59, 59, tzinfo=doctor.timezone)
        appointments = Appointment.objects.filter(doctor=doctor,
                                                  date__gte=from_,
                                                  date__lte=to,
                                                  status__in=['Confirmed', 'Rescheduled'])

        res = {
            'blocks': [],
        }
        for appointment in appointments:
            res['blocks'].append(appointment.date.timestamp())

        if day == 0:
            res['start'] = doctor.sun_start
            res['end'] = doctor.sun_end
        elif day == 1:
            res['start'] = doctor.mon_start
            res['end'] = doctor.mon_end
        elif day == 2:
            res['start'] = doctor.tue_start
            res['end'] = doctor.tue_end
        elif day == 3:
            res['start'] = doctor.wed_start
            res['end'] = doctor.wed_end
        elif day == 4:
            res['start'] = doctor.thu_start
            res['end'] = doctor.thu_end
        elif day == 5:
            res['start'] = doctor.fri_start
            res['end'] = doctor.fri_end
        elif day == 6:
            res['start'] = doctor.sat_start
            res['end'] = doctor.sat_end

        start = doctor.timezone.localize(datetime.datetime.strptime(
            f'{date} {res["start"]}', '%Y-%m-%d %H:%M:%S'))
        end = doctor.timezone.localize(datetime.datetime.strptime(
            f'{date} {res["end"]}', '%Y-%m-%d %H:%M:%S'))

        res['start'] = start.timestamp()
        res['end'] = end.timestamp()

        return Response(res)

    @action(methods=['get'], detail=True)
    def pdf(self, request, pk=None):
        doctor = Doctor.objects.get(id=pk)
        doctor_serializer = DoctorSerializer(doctor, context={'request': request})

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(doctor.first_name)

        context = {
            'request': request,
            'doctor': doctor_serializer.data,
        }

        render_pdf('doctor_pdf.html', response, context=context)
        return response

    @action(methods=['get'], detail=True)
    def available_times_by_day(self, request, pk):
        doctor: Doctor = self.get_object()
        if not request.GET.get('date'):
            return Response({'error': 'date is required'}, status=status.HTTP_400_BAD_REQUEST)
        date = datetime.date.fromisoformat(request.GET.get('date'))

        available_slots = doctor.get_available_times_by_day(date)

        # Return the slots
        return Response(available_slots)

    # @action(methods=['get'], detail=False)
    # def accepting(self, request):
    #     return Response(self.get_serializer(self.get_queryset().filter(
    #         office_is_active=True, accepting_new_patients=True, is_approved=True), many=True).data)


class InsurancePlanViewSet(viewsets.ModelViewSet):
    queryset = InsurancePlan.objects.all()
    serializer_class = InsurancePlanSerializer


class PharmacyViewSet(viewsets.ModelViewSet):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    # .select_related(
    #     'patient').select_related('doctor').order_by('date')
    serializer_class = AppointmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'patient']
    # permission_classes = [permissions.IsAuthenticated].
    permission_classes = [permissions.AllowAny]

    @action(methods=['get'], detail=True)
    def confirm(self, request, pk):
        appointment = Appointment.objects.get(pk=pk)
        appointment.is_confirmed = True
        appointment.is_cancelled = False
        appointment.status = 'Confirmed'
        appointment.save()

        rsa = RescheduleAppointment.objects.get(appointment_1=appointment)
        if rsa:
            rsa.date_confirmed = RequestStatus.APPROVED
            rsa.appointment_2.is_confirmed = False
            rsa.appointment_2.is_cancelled = True
            rsa.appointment_2.status = RequestStatus.CANCELLED
            rsa.appointment_2.save()
            rsa.save()
        rsa = RescheduleAppointment.objects.get(appointment_2=appointment)
        if rsa:
            rsa.date_confirmed = RequestStatus.APPROVED
            rsa.appointment_1.is_confirmed = False
            rsa.appointment_1.is_cancelled = True
            rsa.appointment_1.status = RequestStatus.CANCELLED
            rsa.appointment_1.save()
            rsa.save()

        return JsonResponse(model_to_dict(appointment))

    @action(methods=['get'], detail=True)
    def deny(self, request, pk):
        appointment = Appointment.objects.get(pk=pk)
        appointment.is_confirmed = False
        appointment.is_cancelled = True
        appointment.status = "Denied"
        appointment.save()

        return JsonResponse(model_to_dict(appointment))

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     patients = qs.filter(patient__in=self.request.user.relationship_set.all(
    #     ).values_list('patient_id', flat=True))
    #     doctors = qs.filter(
    #         doctor__in=self.request.user.doctors.values_list('id', flat=True))
    #     return patients | doctors

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'today':
            return AppointmentListSerializer

        return AppointmentSerializer

    def list(self, request, *args, **kwargs):
        from_ = request.query_params.get('from')
        to = request.query_params.get('to')

        queryset = self.get_queryset()
        if from_:
            queryset = queryset.filter(
                date__gte=datetime.datetime.utcfromtimestamp(float(from_)))
        if to:
            queryset = queryset.filter(
                date__lte=datetime.datetime.utcfromtimestamp(float(to)))

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def today(self, request, *args, **kwargs):
        from_ = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        to = datetime.datetime.today().replace(hour=23, minute=59, second=59, microsecond=0)

        queryset = self.get_queryset()
        queryset = queryset.filter(status='Confirmed')
        queryset = queryset.filter(date__gte=from_)
        queryset = queryset.filter(date__lte=to)
        if request.user.is_authenticated:
            if request.user.type == 'Doctor':
                queryset = self.get_queryset().filter(doctor=request.user.doctor)
            elif request.user.type == 'Patient':
                queryset = self.get_queryset().filter(patient=request.user.patient)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def month(self, request):
        from_ = request.query_params.get('from')
        to = request.query_params.get('to')

        queryset = self.get_queryset().values_list('date', flat=True)
        if from_:
            queryset = queryset.filter(
                date__gte=datetime.datetime.utcfromtimestamp(float(from_)))
        if to:
            queryset = queryset.filter(
                date__lte=datetime.datetime.utcfromtimestamp(float(to)))

    #     return Response([date.timestamp() for date in queryset])
# BELOW: It looks like the prev developer is only using POST if there is an actual video appointment.
    @action(methods=['post'], detail=True)
    def createappointment(self, request):
        patient_id = request.POST.get('patient')
        doctor_id = request.POST.get('provider')
        user = request.user
        if request.method == 'POST':
            if request.POST.get(user) and (request.POST.get(patient_id) or request.POST.get(doctor_id)):
                appointment = Appointment()
                appointment.requested_by = request.POST.get('user')
                appointment.patient_id = (patient_id)
                appointment.doctor_id = (doctor_id)
                # appointment.date= request.POST.get('date')
                appointment.duration = request.POST.get('selectedDuration')
                raw_datetime = request.POST.get("date")
                appointment_time = arrow.get(raw_datetime) if raw_datetime else None
                appointment.date = appointment_time
                appointment.type = request.POST.get('type')
                appointment.recurring = request.POST.get('selectedRecurringType')
                # appointment.notes= request.POST.get(patient_id)
                # appointment.questionnaires= request.POST.get(patient_id)
                appointment.status = request.POST.get(patient_id)
                appointment.sent = request.POST.get(patient_id)
                # appointment.pharmacy_id= request.POST.get(patient_id)
                appointment.appointment_type = request.POST.get('selectedAppointmentType')

                appointment.save()
                
                return print(request, 'Appointment Request Saved')  

            else:
                return print(request, 'Something Went Wrong in Appointment [POST] @action')

    # @transaction.atomic
    # def join(self, request, pk):
    #     user = request.user
    #     appointment = self.get_object()

    #     if user.type == 'Doctor':
    #         identity = str(appointment.doctor)
    #     else:
    #         identity = str(appointment.patient)

    #     room = hashids.encode(appointment.id)
    #     token = AccessToken(account_sid, api_key,
    #                         api_secret, identity=identity)
    #     video_grant = VideoGrant(room=room)
    #     # conversations_grant = ChatGrant(service_sid=conversations_service_id)
    #     # token.add_grant(video_grant)
    #     # token.add_grant(conversations_grant)

    #     try:
    #         c = client.conversations.conversations.create(unique_name=room)
    #     except Exception as e:
    #         c = client.conversations.conversations.get(room)

    #     try:
    #         c.participants.create(identity=identity)
    #     except:
    #         pass

    #     return Response({
    #         'name': room,
    #         'token': token.to_jwt(),
    #     })


class RescheduleAppointmentViewSet(viewsets.ModelViewSet):
    queryset = RescheduleAppointment.objects.all()
    serializer_class = RescheduleAppointmentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        appointment_ref = Appointment.objects.get(id=serializer.validated_data['appointment_ref_id'])
        appointment_ref.is_rescheduled = True
        appointment_ref.is_cancelled = False
        appointment_ref.is_confirmed = False
        appointment_ref.status = 'Rescheduled'
        appointment_ref.save()

        return Response(serializer.data)


class SymptomViewSet(viewsets.ModelViewSet):
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer


# class RoomViewSet(viewsets.ViewSet):
#     @action(methods=['post'], detail=True)
#     def recording(self, request, pk):
#         client.video.rooms.get(pk).recording_rules.update({
#             'rules': request.data,
#         })
#         return Response()


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

    def list(self, request, *args, **kwargs):
        doctor = request.query_params.get('doctor')
        queryset = self.get_queryset()
        if doctor:
            queryset = queryset.filter(doctor=doctor)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ValidateNewUser(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format='json'):
        email = request.data.get('email')
        code = request.data.get('code')
        # user = User.objects.filter(email=email, activation_token=code).first()
        user = User.objects.filter(email=email).filter(activation_token=code).first()
        print(request.data.get('email'))
        print(request.data.get('code'))
        print(timezone.now(), user.activation_expired, sep='\n')
        # print(user.pk)
        if user and user.activation_expired >= timezone.now():
            user.activation_expired = None
            print("Success so far.")
            user.is_active = True
            user.save(update_fields=['activation_token', 'activation_expired', 'is_active'])
            return Response('Your account has now been activated.',
                            status=status.HTTP_202_ACCEPTED)
        return Response('Failed to validate the user account', status= status.HTTP_417_EXPECTATION_FAILED)

                            



class ConsultRequestViewSet(viewsets.ModelViewSet):
    queryset = ConsultRequest.objects.all()
    serializer_class = ConsultRequestSerializer

    def list(self, request, *args, **kwargs):
        if request.user.type == 'Doctor':
            doctor = Doctor.objects.get(email=request.user.email)
            queryset = self.get_queryset().filter(sent_to=doctor.id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        elif request.user.type == 'Patient':
            patient = Patient.objects.get(email=request.user.email)
            queryset = self.get_queryset().filter(requester=patient.id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['get', 'post'], detail=True)
    def accept(self, request, pk):
        consult_request = get_object_or_404(ConsultRequest, pk=pk)
        consult_request.is_accepted = True
        consult_request.save()

        patient_user = User.objects.get(email=consult_request.requester.email)

        doctor = Doctor.objects.get(email=consult_request.sent_to.email)
        doctor_user = User.objects.get(email=doctor.email)
        patient_user.doctors.add(doctor)
        doctor_user.patients.add(consult_request.requester)

        return Response('Consult Request Accepted', status=status.HTTP_202_ACCEPTED)

    @action(methods=['get', 'post'], detail=True)
    def refer(self, request, pk):
        consult_request = get_object_or_404(ConsultRequest, pk=pk)
        consult_request.is_referred = True
        consult_request.status = "Referred"
        consult_request.save()

        return Response('Consult Request Referred', status=status.HTTP_202_ACCEPTED)

    @action(methods=['get', 'post'], detail=True)
    def reject(self, request, pk):
        consult_request = get_object_or_404(ConsultRequest, pk=pk)
        consult_request.is_accepted = False
        consult_request.status = "Rejected"
        consult_request.save()

        return Response('Consult Request Rejected', status=status.HTTP_202_ACCEPTED)

    @action(methods=['get', 'post'], detail=True)
    def refer(self, request, pk):
        consult_request = get_object_or_404(ConsultRequest, pk=pk)
        consult_request.is_referred = True
        consult_request.status = "Referred"
        consult_request.save()

        return Response('Consult Request Referred', status=status.HTTP_202_ACCEPTED)



class ReferralRequestViewSet(viewsets.ModelViewSet):
    queryset = ReferralRequest.objects.all()
    serializer_class = ReferralRequestSerializer

    def list(self, request, *args, **kwargs):
        if request.user.type == 'Doctor':
            doctor = Doctor.objects.get(email=request.user.email)
            responses = ReferralRequestResponse.objects.filter(doctor=doctor)
            queryset = self.get_queryset().filter(referralrequestresponse__in=responses)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        elif request.user.type == 'Patient':
            patient = Patient.objects.get(email=request.user.email)
            queryset = self.get_queryset().filter(sender=request.user)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def sent(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(sender=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get', 'post'], detail=True)
    def accept(self, request, pk):
        if request.user.type != "Doctor":
            return Response(status=status.HTTP_400_BAD_REQUEST)

        referral_request = get_object_or_404(ReferralRequest, pk=pk)
        referral_request.is_accepted = True
        referral_request.status = "Accepted"
        referral_request.save()

        patient_user = User.objects.get(email=referral_request.patient.email)

        for doctor in referral_request.doctors.all():
            if request.user.email == doctor.email:
                response = ReferralRequestResponse.objects.filter(referral=referral_request, doctor=doctor)[0]
                response.status = "Accepted"
                response.save()
                doctor_user = User.objects.get(email=doctor.email)
                patient_user.doctors.add(doctor)
                doctor_user.patients.add(referral_request.patient)

        return Response('Referral Request Accepted', status=status.HTTP_202_ACCEPTED)

    @action(methods=['get', 'post'], detail=True)
    def reject(self, request, pk):
        referral_request = get_object_or_404(ReferralRequest, pk=pk)
        referral_request.is_accepted = False
        referral_request.status = "Rejected"
        referral_request.save()

        doctor = Doctor.objects.get(email=request.user.email)
        response = ReferralRequestResponse.objects.filter(referral=referral_request, doctor=doctor)[0]
        response.status = "Rejected"
        response.save()

        return Response('Referral Request Rejected', status=status.HTTP_202_ACCEPTED)



class ReferralRequestResponseViewSet(viewsets.ModelViewSet):
    queryset = ReferralRequestResponse.objects.all()
    serializer_class = ReferralRequestResponseSerializer

    def list(self, request, *args, **kwargs):
        if request.user.type == 'Doctor':
            doctor = Doctor.objects.get(email=request.user.email)
            queryset = self.get_queryset().filter(doctor=doctor)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        elif request.user.type == 'Patient':
            patient = Patient.objects.get(email=request.user.email)
            queryset = self.get_queryset().filter(request__patient=patient)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AppointmentConfirmationViewSet(viewsets.ModelViewSet):
    queryset = AppointmentConfirmation.objects.all()
    serializer_class = AppointmentConfirmationSerializer
    permission_classes = [permissions.AllowAny]


class AssociationViewSet(viewsets.ViewSet):
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.type == "Patient":
            return self.request.user.doctors.all()
        elif self.request.user.type == "Doctor":
            return self.request.user.patients.all()
        else:
            return None

    def list(self, request):
        queryset = self.get_queryset()
        if request.user.type == "Patient":
            serializer = DoctorSerializer(queryset, many=True, context={'request': request})
        elif request.user.type == "Doctor":
            serializer = PatientSerializer(queryset, many=True, context={'request': request})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    def create(self, request, format=None):
        if request.user.type == "Patient":
            doctor = request.data.get('doctor')
            patient = request.user
            if patient.doctors.filter(id=doctor).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                patient.doctors.add(doctor)
                return Response(status=status.HTTP_201_CREATED)
        elif request.user.type == "Doctor":
            patient = request.data.get('patient')
            doctor = request.user
            if doctor.patients.filter(id=patient).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                doctor.patients.add(patient)
                return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, format=None):
        if request.user.type == "Patient":
            doctor = request.data.get('doctor')
            patient = request.user
            patient.doctors.remove(doctor)
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.user.type == "Doctor":
            patient = request.data.get('patient')
            doctor = request.user
            doctor.patients.remove(patient)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

#browser timezone
#def set_timezone(request):
    #if request.method == 'POST':
        #request.session['django_timezone'] = request.POST['timezone']
        #return redirect('/')
    #else:
        #return render(request, 'template.html', {'timezones': pytz.common_timezones})
