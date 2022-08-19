from django.shortcuts import render
# from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.utils import timezone
from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.mixins import LoginRequiredMixin
from django_renderpdf.views import PDFView

from notes.models import ProviderNote
from .serializers import ProviderNoteSerializer

from accounts.models import Doctor, Patient
from accounts import permissions


# Archives entries that are older than 7 days
# ProviderNote.objects.filter(
#     date_created__lte=timezone.now() - timedelta(days=7)).update(archived=True)
class ProviderNoteViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderNoteSerializer
    # permission_classes = [permissions.IsDoctor]

    def get_queryset(self):
        user = self.request.user
        queryset = ProviderNote.objects.filter(author=user)
        return queryset
    #
    # def list(self, request, **kwargs):
    #     queryset = ProviderNote.objects.filter(author=request.user)
    #     return Response(queryset)

    # @action(methods=['post'], detail=False)
    # def doctor_notes(self, request):
    #     # We will get the doctor ID and filter
    #     pk = request.data.get('id')
    #     patient_id = request.data.get('patient_id')
    #     doctor = Doctor.objects.get(pk=pk)
    #     patient = Patient.objects.get(pk=patient_id)

    #     # Get list of foreign keys and filter by patient id 
    #     provider_notes = doctor.ProviderNote_set.filter(patient__pk=patient_id)
    #     data = {
    #         'patient_first_name': patient.first_name,
    #         'patient_last_name': patient.last_name,
    #         'provider_notes': provider_notes,
    #     }
         
    #     return Response(data, status=status.HTTP_200_OKAY)

    # @action(methods=['get'], detail=True)
    # def doctor_all_notes_each_patient(self, request):
    #     # We will get the doctor ID and filter
    #     pk = request.data.get('id')
    #     patient_id = request.data.get('patient_id')
    #     doctor = Doctor.objects.get(pk=pk)
    #     patient = Patient.objects.get(pk=patient_id)

    #     # Get list of foreign keys and filter by patient id 
    #     provider_notes = doctor.ProviderNote_set.filter(patient__pk=patient_id)
    #     data = {
    #         'patient_first_name': patient.first_name,
    #         'patient_last_name': patient.last_name,
    #         'provider_notes': provider_notes,
    #     }
         
    #     return Response(data, status=status.HTTP_200_OKAY)

    # @action(methods=['post', 'put', 'delete'], detail=False)
    # def note_detail(request, pk):
    #             # find note by pk (id)
    #         try: 
    #             data = ProviderNote.objects.get(pk=pk) 
    #             return Response(data, status=status.HTTP_200_OKAY)
    #         except ProviderNote.DoesNotExist: 
    #             return Response({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND)


class DownloadViewSet(PDFView):
    # LoginRequiredMixin, 
    prompt_download = True
    template_name = 'notes/pdf.html'
    download_name = 'note.pdf'

    # @property
    # def download_name(self) -> str:
    #     return f"journal_{self.object.pk}.pdf"

    def get_context_data(self, *args, **kwargs):
        """Pass some extra context to the template."""
        context = super().get_context_data(**kwargs)
        context['object'] = get_object_or_404(ProviderNote, pk=kwargs['pk'])
        return context
