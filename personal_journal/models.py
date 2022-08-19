from django.db import models
from accounts.models import Patient, Doctor, User
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.deletion import DO_NOTHING

class JournalEntry(models.Model):
    options = (
        ('archived', 'Archived'),
        ('editable', 'Editable'),
    )
    title = models.CharField(max_length=250)
    excerpt = models.TextField(null=True)
    content = models.TextField()
    archived = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    status = models.CharField(max_length=10, choices=options, default='editable')
    shared_with = models.ForeignKey(Doctor, blank=True, null=True,  on_delete=DO_NOTHING)
    date_shared = models.DateTimeField(auto_now=True, null=True)

    # models.PROTECT keeps provider from being deleted if there are journal entries associated with it
    provider = models.ForeignKey(Doctor, on_delete=models.PROTECT, null=True, related_name='journal_entries_for_provider')
    # Eventually turn off profile instead of deleting
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal_entries')

    class Meta:
        ordering = ['-date_created']
        verbose_name_plural = 'Journal Entries'

    def __str__(self):
        return self.title

    def clean(self):
        # Converts name to a slug if not already a valid slug for creating journal entries
        self.slug = slugify(self.title) if not self.slug or self.slug != slugify(self.title) else self.slug

    def save(self, *args, **kwargs):
        self.full_clean()  # Calls clean() when saving data in the DB
        super().save(*args, **kwargs)
