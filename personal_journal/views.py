from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import query
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.response import Response
# from rest_framework.decorators import action
# from rest_framework.request import Request
from django.contrib.auth.mixins import LoginRequiredMixin
from django_renderpdf.views import PDFView


from personal_journal.models import JournalEntry
from .serializers import JournalEntrySerializer


# Archives entries that are older than 7 days
# JournalEntry.objects.filter(
#     date_created__lte=timezone.now() - timedelta(days=7)).update(archived=True)

# Below: Automatically updates url to show the correct page depending on the api called.
class JournalEntryViewSet(viewsets.ModelViewSet):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer


class DownloadViewSet(PDFView):
    # LoginRequiredMixin, 
    prompt_download = True
    template_name = 'personal_journal/pdf.html'
    download_name = 'journal.pdf'

    # @property
    # def download_name(self) -> str:
    #     return f"journal_{self.object.pk}.pdf"

    def get_context_data(self, *args, **kwargs):
        """Pass some extra context to the template."""
        context = super().get_context_data(**kwargs)
        context['object'] = get_object_or_404(JournalEntry, pk=kwargs['pk'])
        return context


# class JournalEntryListView(ListView):
#     model = JournalEntry
#     context_object_name = 'journal_entry_list'
#     queryset = JournalEntry.objects.filter(archived=False)
#     # template_name = 'personal_journal/index.html'


# class ArchivedJournalEntryListView(ListView):
#     model = JournalEntry
#     context_object_name = 'archived_journal_entry_list'
#     queryset = JournalEntry.objects.filter(archived=True)
#     # template_name = 'personal_journal/archived.html'


# # Can combine DetailView and ListView: https://stackoverflow.com/questions/41287431/django-combine-detailview-and-listview
# class JournalEntryDetailView(DetailView):
#     model = JournalEntry
#     context_object_name = 'journal_entry'
#     # template_name = 'personal_journal/journal_detail.html'


# # https://koenwoortman.com/python-django-set-current-user-create-view/
# class JournalEntryCreateView(LoginRequiredMixin, CreateView):
#     model = JournalEntry
#     success_message = 'Journal Successfully Created'

#     fields = ['title', 'provider', 'excerpt', 'content']
#     template_name = 'personal_journal/create_journal.html'

#     # Will need to add the authenticated user that created the journal entry
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse('journal-detail', kwargs={'slug': self.object.slug})


# class JournalEntryUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
#     model = JournalEntry
#     fields = ['title', 'provider', 'excerpt', 'content']
#     context_object_name = 'journal_entry'
#     # template_name = 'personal_journal/update_journal.html'
#     success_message = 'Journal Successfully Updated'

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

#     def get_success_url(self): # Used for Django frontend templates only.
#         return reverse('update-journal', kwargs={'slug': self.object.slug})

#     def get_object(self, *args, **kwargs):
#         return get_object_or_404(self.model, slug=self.kwargs['slug'])

