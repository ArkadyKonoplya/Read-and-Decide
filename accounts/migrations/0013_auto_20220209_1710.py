# Generated by Django 3.2.9 on 2022-02-10 00:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20220105_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='is_cancelled',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='is_rescheduled',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='lockedresource',
            name='shared_with_telepsycrx',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='lockedresource',
            name='shared_with',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.doctor'),
        ),
        migrations.AlterField(
            model_name='lockedresource',
            name='uploaded_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ReferralRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.TextField(null=True)),
                ('requested_date', models.DateField(null=True)),
                ('requested_time', models.TimeField(null=True)),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.patient')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('sent_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='ConsultRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_accepted', models.BooleanField(default=False, null=True)),
                ('is_referred', models.BooleanField(default=False, null=True)),
                ('patient_full_name', models.CharField(max_length=100, null=True)),
                ('details', models.TextField(null=True)),
                ('requested_date', models.DateField(null=True)),
                ('requested_time', models.TimeField(null=True)),
                ('requester', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.patient')),
                ('sent_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.doctor')),
            ],
        ),
    ]
