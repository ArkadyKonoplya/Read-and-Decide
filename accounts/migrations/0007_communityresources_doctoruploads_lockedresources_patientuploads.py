# Generated by Django 3.2.9 on 2021-12-26 05:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20211221_1929'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientUploads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_type', models.CharField(max_length=10, null=True)),
                ('file_subject', models.CharField(max_length=100, null=True)),
                ('file', models.URLField(null=True)),
                ('uploaded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.patient')),
            ],
        ),
        migrations.CreateModel(
            name='LockedResources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_type', models.CharField(max_length=10, null=True)),
                ('file_subject', models.CharField(max_length=100, null=True)),
                ('file', models.URLField(null=True)),
                ('shared_with', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('uploaded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.patient')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorUploads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_approved', models.BooleanField(null=True)),
                ('file_type', models.CharField(max_length=10, null=True)),
                ('file_subject', models.CharField(max_length=100, null=True)),
                ('file', models.URLField(null=True)),
                ('uploaded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='CommunityResources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_type', models.CharField(max_length=10, null=True)),
                ('file_subject', models.CharField(max_length=100, null=True)),
                ('file', models.URLField(null=True)),
                ('uploaded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.doctor')),
            ],
        ),
    ]
