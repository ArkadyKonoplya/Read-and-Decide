from django.db.models import TextChoices


# Accessing in models examples:
# SomeField(choices=Relationship.choices, default=Relationship.DAUGHTER)

class UserType(TextChoices):
    PATIENT = 'Patient'
    DOCTOR = 'Doctor'
    CASE_MANAGER = 'Case Manager'


class Gender(TextChoices):
    MALE = 'Male'
    FEMALE = 'Female'
    TRANS = 'Trans'
    NON_BINARY = 'Non-binary'

class SubscriptionType(TextChoices):
    Free_Membership = 'Free_Membership'
    Medication_N_CareCounseling = 'Medication_CareCounseling'
    Medication_Therapy = 'Medication_Therapy'
    Therapy  = 'Therapy'
    CareCounseling = 'Care_Counseling'
    Economy1_Texting = 'Economy1_Texting'
    Economy2_Texting_Journal = 'Economy2_Texting_Journal'


class HeightUnit(TextChoices):
    FT = 'ft'
    CM = 'cm'


class WeightUnit(TextChoices):
    LB = 'lb'
    KG = 'kg'

class DateChosen(TextChoices):
    date_1 = 'Date_1'
    date_2 = 'Date_2'


class RelationshipType(TextChoices):
    ME = 'Me'
    DAUGHTER = 'Daughter'
    DOMESTIC_PARTNER = 'Domestic Partner'
    HUSBAND = 'Husband'
    OTHER = 'Other'
    PARENT = 'Parent'
    SON = 'Son'

class Recurring(TextChoices):
    NO = 'No'
    DAILY = 'Daily'
    WEEKLY = 'Weekly'
    BI_WEEKLY = 'Bi-Weekly'
    MONTHLY = 'Monthly'
    BI_MONTHLY = 'Bi-Monthly'
    ANNUALLY = 'Annually'

class InvitationStatus(TextChoices):
    INVITED = 'Invited'
    ACCEPTED = 'Accepted'
    DENIED = 'Denied'


Duration = [
    (30, "30"),
    (60, "60"),
    (120, "120"),
]

TITLES = [
    ('MD - Psychiatry', 'MD - Psychiatry'),
    ('MD - Neurology', 'MD - Neurology'),
    ('MD - Child and Adolescent Psychiatry', 'MD - Child and Adolescent Psychiatry'),
    ('MD - Adult Psychiatry', 'MD - Adult Psychiatry'),
    ('MD - Geriatric Psychiatry', 'MD - Geriatric Psychiatry'),
    ('MD - Addiction Psychiatry', 'MD - Addiction Psychiatry'),
    ('MD - Emergency Psychiatry', 'MD - Emergency Psychiatry'),
    ('DO - Psychiatry', 'DO - Psychiatry'),
    ('DO - Neurology', 'DO - Neurology'),
    ('DO - Child and Adolescent Psychiatry', 'DO - Child and Adolescent Psychiatry'),
    ('DO - Adult Psychiatry', 'DO - Adult Psychiatry'),
    ('DO - Geriatric Psychiatry', 'DO - Geriatric Psychiatry'),
    ('DO - Addiction Psychiatry', 'DO - Addiction Psychiatry'),
    ('DO - Emergency Psychiatry', 'DO - Emergency Psychiatry'),
    ('APRN - Psychiatry', 'APRN - Psychiatry'),
    ('PA - Psychiatry', 'PA - Psychiatry'),
    ('PHD - Psychology', 'PHD - Psychology'),
    ('LCSW - Therapy', 'LCSW - Therapy'),
]


class BoardCertifiedSpecialty(TextChoices):
    FAMILY_MEDICINE = 'Family Medicine'
    INTERNAL_MEDICINE = 'Internal Medicine'
    EMERGENCY_MEDICINE = 'Emergency Medicine'
    PEDIATRICS = 'Pediatrics'


class AppointmentStatus(TextChoices):
    REQUESTED = 'Requested'
    CONFIRMED = 'Confirmed'
    RESCHEDULED = 'Rescheduled'
    DENIED = 'Denied'
