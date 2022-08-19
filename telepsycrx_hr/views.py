from django.shortcuts import render
from rest_framework import viewsets
from telepsycrx_hr.models import UserConcern
from telepsycrx_hr.serializer import UserConcernSerializer

class UserConcernViewSet(viewsets.ModelViewSet):
    queryset = UserConcern.objects.all()
    serializer_class = UserConcernSerializer
