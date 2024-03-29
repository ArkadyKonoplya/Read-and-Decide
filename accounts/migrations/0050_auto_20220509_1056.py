# Generated by Django 3.2.9 on 2022-05-09 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0049_auto_20220506_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lockedresource',
            name='shared_with_telepsycrx',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='AnnotatedResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Patient', 'Patient'), ('Doctor', 'Doctor'), ('Case Manager', 'Case Manager')], default='Doctor', max_length=20)),
                ('file_type', models.CharField(max_length=10, null=True)),
                ('file_subject', models.CharField(max_length=100, null=True)),
                ('file', models.FileField(null=True, upload_to='doctors/annotatedResponses')),
                ('shared_with_telepsycrx', models.BooleanField(default=False)),
                ('shared_with', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.patient')),
                ('uploaded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.doctor')),
            ],
        ),
    ]
