# Generated by Django 3.2.9 on 2021-12-21 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='family_low_blood_pressure',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='patient',
            name='low_blood_pressure',
            field=models.BooleanField(default=False),
        ),
    ]