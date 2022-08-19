from django.db import models
from django.db import models
from accounts.models import User, Doctor, Patient, UserType
from telePsycRxEmployees.models import TelePsycRxEmployee
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.deletion import DO_NOTHING
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField  # This is specific to Postgres


class PatientWaitList(models.Model):

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    patient_id = models.IntegerField(null=True)
    first_name = models.CharField(_("first name"), max_length=150, null=True)
    last_name = models.CharField(_("last name"), max_length=150, null=True)
    email = models.EmailField(null=True)
    state_of_residence = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    # slug = models.SlugField(max_length=250, unique=True)

    # class Meta:
    


class DoctorWaitList(models.Model):

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(_("first name"), max_length=150, null=True)
    last_name = models.CharField(_("last name"), max_length=150, null=True)
    email = models.EmailField(null=True)
    state_of_residence = models.CharField(max_length=200, null=True, blank=True)
    states_of_license = ArrayField(
        models.CharField(max_length=300), null=True, blank=True
    )
    doctor_id = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    # slug = models.SlugField(max_length=250, unique=True)

    # class Meta:
   


class UserSuggestion(models.Model):

    date_submitted = models.DateTimeField(auto_now=True)
    made_by = models.ForeignKey(User, null=True, on_delete=DO_NOTHING)
    user_type = models.CharField(
        max_length=20, choices=UserType.choices, default="Patient"
    )
    title = models.CharField(max_length=250)
    details = models.TextField(null=True)


class UserReview(models.Model):

    date_submitted = models.DateTimeField(auto_now=True)
    made_by = models.ForeignKey(User, null=True, on_delete=DO_NOTHING)
    user_type = models.CharField(
        max_length=20, choices=UserType.choices, default="Patient"
    )
    title = models.CharField(max_length=250)
    details = models.TextField(null=True)


# class Role(models.Model):
#     statusOptions = (
#         ('temporary', 'Temporary'),
#         ('permanent', 'Permanent'),
#         ('occasional', 'Occasional'),
#     )
#     EmTyOptions = (
#         ('Full-time', 'Full-time'),
#         ('part-time', 'Part-time'),
#         ('occasional', 'Occasional'),
#     )

#     title = models.CharField(max_length=250)
#     description = models.TextField(null=True)
#     is_active = models.BooleanField(default=False)
#     department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True)
#     division = models.ForeignKey(Division, on_delete=models.PROTECT, null=True)
#     slug = models.SlugField(max_length=250, unique=True)
#     status = models.CharField(max_length=10, choices=statusOptions, default='temporary')
#     employment_workType = models.CharField(max_length=10, choices=EmTyOptions, default='full-time')

#     class Meta:
#         # ordering = ['-date_created']
#         verbose_name_plural = 'Roles'

#     def __str__(self):
#         return self.title

#     def clean(self):
#         # Converts name to a slug if not already a valid slug for creating journal entries
#         self.slug = slugify(self.title) if not self.slug or self.slug != slugify(self.title) else self.slug

#     def save(self, *args, **kwargs):
#         self.full_clean()  # Calls clean() when saving data in the DB
#         super().save(*args, **kwargs)


# class TelePsycRxEmloyee(models.Model):
#     StatOptions = (
#         ('current', 'Current'),
#         ('new hire', 'New Hire'),
#         ('former', 'Former'),
#         ('terminated', 'Terminated'),
#     )
#     D_Options = (
#         ('voluntary', 'Voluntary'),
#         ('mandated', 'Mandated'),
#     )
#     user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
#     title = models.CharField(max_length=250)
#     Role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True)
#     hire_date = models.DateTimeField(null=True)
#     contract_start_date = models.DateTimeField(auto_now=True, null=True)
#     contract_end_date = models.DateTimeField(auto_now=True, null=True)
#     is_active = models.BooleanField(default=False)
#     department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True)
#     division = models.ForeignKey(Division, on_delete=models.PROTECT, null=True)
#     archived = models.BooleanField(default=False)
#     slug = models.SlugField(max_length=250, unique=True)
#     status = models.CharField(max_length=10, choices=StatOptions, default='null')
#     personal_email = models.CharField(max_length=250)
#     company_email = models.CharField(max_length=250)
#     auth_to_share = models.BooleanField(default=False)
#     dismissal = models.CharField(max_length=10, choices=D_Options, default='null')

#     class Meta:
#         # ordering = ['-date_created']
#         verbose_name_plural = 'Employees'

#     def __str__(self):
#         return self.title

#     def clean(self):
#         # Converts name to a slug if not already a valid slug for creating journal entries
#         self.slug = slugify(self.title) if not self.slug or self.slug != slugify(self.title) else self.slug

#     def save(self, *args, **kwargs):
#         self.full_clean()  # Calls clean() when saving data in the DB
#         super().save(*args, **kwargs)
