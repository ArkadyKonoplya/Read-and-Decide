from django.db import models
from accounts.models import User, Doctor, Patient


class Billing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)


class Transaction(models.Model):
    billing = models.ForeignKey(Billing, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    time = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    type = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    txn_id = models.CharField(max_length=100)


# class Transactions(models.Model):
#     elavons_response = (
#         # ('unpaid', 'Unpaid'),
#         # ('initiated', 'Initiated'),
#         # ('pending', 'Pending'),
#         # ('paid', 'Paid'),
#         # ('delinquent', 'Delinquent'),
#         ('payment_successful', 'payment_successful'),
#         ('declined', 'declined'),
#     )
#
#     subscription_types =(
#         ('Free_Membership', 'Free_Membership'),
#         ('Medication_N_CareCounseling', 'Medication_N_CareCounseling'),
#         ('Therapy', 'Therapy'),
#         ('Medication_Therapy', 'Medication_Therapy'),
#     )
#     customer = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patients')
#     subscription_type = models.CharField(max_length=100, choices=subscription_types, default='Free_Membership')
#     date_transaction = models.DateTimeField(auto_now=True, null=True)
#     status = models.CharField(max_length=100, choices=elavons_response, default='null')
#     # shared_with = models.ForeignKey(TelePsycRxEmployee, on_delete=models.PROTECT, null=True)
#     # date_shared = models.DateTimeField(auto_now=True, null=True)
#     # archived = models.BooleanField(default=False)
#     transaction_type = models.CharField(max_length=250, null=True)
#     amount = models.FloatField(null=True)
#     transaction_id = models.CharField(max_length=250, null=True)
#
#
#
#
#     # provider = models.ForeignKey(Doctor, on_delete=models.PROTECT, null=True)
#
#
#
#     class Meta:
#         # ordering = ['-date_created']
#         verbose_name_plural = 'Transactions'
#
#     def __str__(self):
#         return self.title
#
#     def clean(self):
#         # Converts name to a slug if not already a valid slug for creating journal entries
#         self.slug = slugify(self.title) if not self.slug or self.slug != slugify(self.title) else self.slug
#
#     def save(self, *args, **kwargs):
#         self.full_clean()  # Calls clean() when saving data in the DB
#         super().save(*args, **kwargs)
#
#
