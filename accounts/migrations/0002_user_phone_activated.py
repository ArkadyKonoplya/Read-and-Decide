# Generated by Django 3.2.9 on 2021-12-11 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_activated',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]