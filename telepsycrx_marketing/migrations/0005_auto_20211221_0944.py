# Generated by Django 3.2.9 on 2021-12-21 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telepsycrx_marketing', '0004_auto_20211220_2154'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctorwaitlist',
            old_name='doctor_id',
            new_name='state_of_license',
        ),
        migrations.RenameField(
            model_name='patientwaitlist',
            old_name='patient_id',
            new_name='state_of_residence',
        ),
    ]
