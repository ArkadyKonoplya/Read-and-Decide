# Generated by Django 3.2.9 on 2022-08-01 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0064_auto_20220731_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='phone_activation_expired',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
