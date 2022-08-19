# Generated by Django 3.2.9 on 2022-04-02 22:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_consultrequest_appointment_for'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consultrequest',
            name='sent_to',
        ),
        migrations.AddField(
            model_name='consultrequest',
            name='sent_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='consulted_to', to='accounts.doctor'),
        ),
    ]