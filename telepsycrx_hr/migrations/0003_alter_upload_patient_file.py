# Generated by Django 3.2.9 on 2021-12-27 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_appointment_pharmacy'),
        ('telepsycrx_hr', '0002_auto_20211225_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='patient_file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.patientupload'),
        ),
    ]
