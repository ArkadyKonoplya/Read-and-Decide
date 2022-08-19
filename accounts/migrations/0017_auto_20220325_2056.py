# Generated by Django 3.2.9 on 2022-03-26 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_appointmentconfirmation'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='is_on_waitList',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='subscription_type',
            field=models.CharField(blank=True, choices=[('Free_Membership', 'Free Membership'), ('Medication_N_CareCounseling', 'Medication N Carecounseling'), ('Medication_Therapy', 'Medication Therapy'), ('Therapy', 'Therapy')], max_length=70, null=True),
        ),
    ]
