# Generated by Django 3.2.9 on 2021-12-26 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('telepsycrx_hr', '0001_initial'),
        ('accounts', '0007_communityresources_doctoruploads_lockedresources_patientuploads'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PatientUploads',
            new_name='CommunityResource',
        ),
        migrations.RenameModel(
            old_name='DoctorUploads',
            new_name='DoctorUpload',
        ),
        migrations.RenameModel(
            old_name='LockedResources',
            new_name='LockedResource',
        ),
        migrations.RenameModel(
            old_name='CommunityResources',
            new_name='PatientUpload',
        ),
        migrations.AlterField(
            model_name='communityresource',
            name='uploaded_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.doctor'),
        ),
        migrations.AlterField(
            model_name='patientupload',
            name='uploaded_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.patient'),
        ),
    ]
