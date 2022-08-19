from django.db import models
from accounts.models import Doctor, Patient, User
from django.utils import timezone
from django.utils.text import slugify


class ProviderNote(models.Model):
    options = (
        ('archived', 'Archived'),
        ('editable', 'Editable'),
    )
    session_date = models.DateField(null=True)
    session_time = models.TimeField(null=True)
    note = models.TextField()
    archived = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=250, unique=False, null=True, blank=True)
    status = models.CharField(max_length=10, choices=options, default='editable')
    date_shared = models.DateTimeField(auto_now=True, null=True)

    # models.PROTECT keeps provider from being deleted if there are journal entries associated with it
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, null=True, related_name='provider_patient_notes')
    # Eventually turn off profile instead of deleting
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='provider_notes')

    class Meta:
        ordering = ['-date_created']
        verbose_name_plural = 'Provider Notes'

    def __str__(self):
        return f"{self.patient} {self.session_date} {self.session_time}"
    
    def clean(self):
        # Converts name to a slug if not already a valid slug for creating journal entries
        self.slug = slugify(self.patient, self.session_date) if not self.slug or self.slug != slugify(
            self.patient, self.session_date) else self.slug

    def save(self, *args, **kwargs):
        self.full_clean()  # Calls clean() when saving data in the DB
        super().save(*args, **kwargs)
