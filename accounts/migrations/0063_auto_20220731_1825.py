# Generated by Django 3.2.9 on 2022-08-01 01:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0062_merge_0055_auto_20220610_1302_0061_auto_20220628_1743'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='activation_expired',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='activation_token',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='phone_activation_expired',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='phone_activation_token',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='activation_expired',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='activation_token',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='phone_activation_expired',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='phone_activation_token',
        ),
    ]