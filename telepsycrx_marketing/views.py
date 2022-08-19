from django.shortcuts import render
from rest_framework import viewsets, permissions
from telepsycrx_marketing.models import UserSuggestion, UserReview, DoctorWaitList, PatientWaitList
from telepsycrx_marketing.serializer import UserSuggestionSerializer, UserReviewSerializer, DoctorWaitListSerializer, PatientWaitListSerializer

class UserSuggestionViewSet(viewsets.ModelViewSet):
    queryset = UserSuggestion.objects.all()
    serializer_class = UserSuggestionSerializer


class UserReviewViewSet(viewsets.ModelViewSet):
    queryset = UserReview.objects.all()
    serializer_class = UserReviewSerializer


class DoctorWaitListViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = DoctorWaitList.objects.all()
    serializer_class = DoctorWaitListSerializer

class PatientWaitListViewSet(viewsets.ModelViewSet):
    queryset = PatientWaitList.objects.all()
    serializer_class = PatientWaitListSerializer