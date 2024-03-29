# Generated by Django 3.2.9 on 2022-03-17 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0016_appointmentconfirmation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_name', models.CharField(max_length=20)),
                ('session_key', models.CharField(max_length=20)),
                ('date', models.DateTimeField(null=True)),
                ('duration', models.IntegerField(null=True)),
                ('session_start', models.DateTimeField(null=True)),
                ('session_duration', models.IntegerField(null=True)),
                ('recording_url', models.CharField(max_length=100, null=True)),
                ('recording_status', models.CharField(choices=[('Not Available', 'Not Available'), ('Processing', 'Processing'), ('Completed', 'Completed')], max_length=20, null=True)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.appointment')),
            ],
        ),
    ]
