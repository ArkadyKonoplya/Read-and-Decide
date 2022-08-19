from django.db import models
from accounts.models import User, Doctor, Patient
from django.utils import timezone
from django.utils.text import slugify

class Division(models.Model):

    title = models.CharField(max_length=250)
    description = models.TextField(null=True)
    is_active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        # ordering = ['-date_created']
        verbose_name_plural = 'Divisions'

    def __str__(self):
        return self.title

    def clean(self):
        # Converts name to a slug if not already a valid slug for creating journal entries
        self.slug = slugify(self.title) if not self.slug or self.slug != slugify(self.title) else self.slug

    def save(self, *args, **kwargs):
        self.full_clean()  # Calls clean() when saving data in the DB
        super().save(*args, **kwargs)

class Department(models.Model):

    title = models.CharField(max_length=250)
    description = models.TextField(null=True)
    is_active = models.BooleanField(default=False)
    division = models.ForeignKey(Division, on_delete=models.PROTECT, null=True)
    slug = models.SlugField(max_length=250, unique=True)
    # status = models.CharField(max_length=10, choices=statusOptions, default='temporary')

    class Meta:
        # ordering = ['-date_created']
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.title

    def clean(self):
        # Converts name to a slug if not already a valid slug for creating journal entries
        self.slug = slugify(self.title) if not self.slug or self.slug != slugify(self.title) else self.slug

    def save(self, *args, **kwargs):
        self.full_clean()  # Calls clean() when saving data in the DB
        super().save(*args, **kwargs)

class Role(models.Model):
    statusOptions = (
        ('temporary', 'Temporary'),
        ('permanent', 'Permanent'),
        ('occasional', 'Occasional'),
    )
    EmTyOptions = (
        ('Full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('occasional', 'Occasional'),
    )

    title = models.CharField(max_length=250)
    description = models.TextField(null=True)
    is_active = models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True)
    division = models.ForeignKey(Division, on_delete=models.PROTECT, null=True)
    slug = models.SlugField(max_length=250, unique=True)
    status = models.CharField(max_length=10, choices=statusOptions, default='temporary')
    employment_workType = models.CharField(max_length=10, choices=EmTyOptions, default='full-time')

    class Meta:
        # ordering = ['-date_created']
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.title

    def clean(self):
        # Converts name to a slug if not already a valid slug for creating journal entries
        self.slug = slugify(self.title) if not self.slug or self.slug != slugify(self.title) else self.slug

    def save(self, *args, **kwargs):
        self.full_clean()  # Calls clean() when saving data in the DB
        super().save(*args, **kwargs)


class TelePsycRxEmployee(models.Model):
    StatOptions = (
        ('current', 'Current'),
        ('new hire', 'New Hire'),
        ('former', 'Former'),
        ('terminated', 'Terminated'),
    )
    D_Options = (
        ('voluntary', 'Voluntary'),
        ('mandated', 'Mandated'),
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    title = models.CharField(max_length=250)
    Role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True)
    hire_date = models.DateTimeField(null=True)
    contract_start_date = models.DateTimeField(auto_now=True, null=True)
    contract_end_date = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True)
    division = models.ForeignKey(Division, on_delete=models.PROTECT, null=True)
    archived = models.BooleanField(default=False)
    slug = models.SlugField(max_length=250, unique=True)
    status = models.CharField(max_length=10, choices=StatOptions, default='null')
    personal_email = models.CharField(max_length=250)
    company_email = models.CharField(max_length=250)
    auth_to_share = models.BooleanField(default=False)
    dismissal = models.CharField(max_length=10, choices=D_Options, default='null')

    class Meta:
        # ordering = ['-date_created']
        verbose_name_plural = 'Employees'

    def __str__(self):
        return self.title

    def clean(self):
        # Converts name to a slug if not already a valid slug for creating journal entries
        self.slug = slugify(self.title) if not self.slug or self.slug != slugify(self.title) else self.slug

    def save(self, *args, **kwargs):
        self.full_clean()  # Calls clean() when saving data in the DB
        super().save(*args, **kwargs)

# class Transactions(models.Model):
#     options = (
#         ('unpaid', 'Unpaid'),
#         ('initiated', 'Initiated'),
#         ('pending', 'Pending'),
#         ('paid', 'Paid'),
#         ('delinquent', 'Delinquent'),
#     )
#     customer = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patients')
#     payment_type = models.CharField(max_length=250)
#     session_date = models.DateTimeField(auto_now=True)
#     session_time = models.DateTimeField(auto_now_add=True)
#     session_duration = models.IntegerField(null=True)
#     slug = models.SlugField(max_length=250, unique=True)
#     status = models.CharField(max_length=10, choices=options, default='null')
#     shared_with = models.ForeignKey(TelePsycRxEmloyee, on_delete=models.PROTECT, null=True)
#     date_shared = models.DateTimeField(auto_now=True, null=True)
#     archived = models.BooleanField(default=False)
#     provider = models.ForeignKey(Doctor, on_delete=models.PROTECT, null=True)



#     class Meta:
#         # ordering = ['-date_created']
#         verbose_name_plural = 'Transactions'

#     def __str__(self):
#         return self.title

#     def clean(self):
#         # Converts name to a slug if not already a valid slug for creating journal entries
#         self.slug = slugify(self.title) if not self.slug or self.slug != slugify(self.title) else self.slug

#     def save(self, *args, **kwargs):
#         self.full_clean()  # Calls clean() when saving data in the DB
#         super().save(*args, **kwargs)

