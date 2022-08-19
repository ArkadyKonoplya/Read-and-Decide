
# from django.urls import path
from rest_framework import routers

from telepsycrx_hr.views import (
    # JournalEntryListView,
    # ArchivedJournalEntryListView,
    # JournalEntryDetailView,
    # JournalEntryCreateView,
    # JournalEntryUpdateView,
    UserConcernViewSet
)

router = routers.DefaultRouter()
router.register('hr-directories', UserConcernViewSet)

urlpatterns = [
#     path('', JournalEntryListView.as_view(), name='personal-journal'),
#     path('archived/', ArchivedJournalEntryListView.as_view(), name='archived-entries'),
#     path('journal_entry/<slug:slug>', JournalEntryDetailView.as_view(), name='journal-detail'),
#     path('create_journal_entry/', JournalEntryCreateView.as_view(), name='create-journal'),
#     path('update_journal_entry/<slug:slug>', JournalEntryUpdateView.as_view(), name='update-journal'),
]

urlpatterns += router.urls

