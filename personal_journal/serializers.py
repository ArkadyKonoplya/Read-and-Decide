from rest_framework import serializers
# from rest_framework.request import Request
from personal_journal.models import JournalEntry


class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ('url',
                  'id',
                  'author',
                  'provider',
                  'title',
                  'excerpt',
                  'content',
                  'archived')
