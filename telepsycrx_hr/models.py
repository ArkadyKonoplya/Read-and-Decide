
from django.db import models
from django.db.models.deletion import DO_NOTHING
from accounts.models import User, UserType
# from telePsycRxEmployees.models import TelePsycRxEmployee
# from django.utils import timezone
# from django.utils.text import slugify

class UserConcern(models.Model):

    date_submitted = models.DateTimeField(auto_now=True)
    made_by = models.ForeignKey(User, null=True, on_delete=DO_NOTHING)
    user_type = models.CharField(max_length=20, choices=UserType.choices, default='Patient')
    title = models.CharField(max_length=250)
    details = models.TextField(null=True)
    is_resolved = models.BooleanField(null=True, default=False)
    files_requested_by_telepsycrx = models.BooleanField(null=True, default=False)



# class ApprovedDoctor(models.Model):

#     doctor_id = models.ForeignKey(Doctor, on_delete=models.PROTECT, null=True)
#     specialty = models.CharField(max_length=10, null=True)
#     description = models.TextField(null=True)
#     is_active = models.BooleanField(default=False)
#     is_accepting_patients = models.BooleanField(null=True)


# class Upload(models.Model):

#     date_shared = models.DateField(null=True)
#     shared_with = models.ForeignKey(User, on_delete=models.PROTECT, null=True) #Is there a way of making this an array of user ids?
#     is_active = models.BooleanField(null=True)

#     is_patient= models.BooleanField(default=False, null=True)
#     patient_id = models.ForeignKey(Patient, on_delete=models.PROTECT, null=True)
#     patient_file = models.ForeignKey(PatientUpload, on_delete=models.PROTECT, null=True)

#     doctor_id = models.ForeignKey(Doctor, on_delete=models.PROTECT, null=True)
#     is_doctor= models.BooleanField(default=False, null=True)
#     doctor_file = models.ForeignKey(DoctorUpload, on_delete=models.PROTECT, null=True)



# class PatientUploads(models.Model):

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