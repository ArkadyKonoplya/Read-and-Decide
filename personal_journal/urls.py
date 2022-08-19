
from django.urls import path
from rest_framework import routers

from personal_journal.views import (
    # JournalEntryListView,
    # ArchivedJournalEntryListView,
    # JournalEntryDetailView,
    # JournalEntryCreateView,
    # JournalEntryUpdateView,
    JournalEntryViewSet,
    DownloadViewSet
)

router = routers.DefaultRouter()
router.register('journal-entries', JournalEntryViewSet)

urlpatterns = [
    path('pdf/<pk>/', DownloadViewSet.as_view(), name='pdf'),
#     path('', JournalEntryListView.as_view(), name='personal-journal'),
#     path('archived/', ArchivedJournalEntryListView.as_view(), name='archived-entries'),
#     path('journal_entry/<slug:slug>', JournalEntryDetailView.as_view(), name='journal-detail'),
#     path('create_journal_entry/', JournalEntryCreateView.as_view(), name='create-journal'),
#     path('update_journal_entry/<slug:slug>', JournalEntryUpdateView.as_view(), name='update-journal'),
]

urlpatterns += router.urls

