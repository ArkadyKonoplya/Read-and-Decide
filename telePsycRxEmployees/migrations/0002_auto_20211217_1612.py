# Generated by Django 3.2.9 on 2021-12-17 23:12

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('telePsycRxEmployees', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TelePsycRxEmloyee',
            new_name='TelePsycRxEmployee',
        ),
        migrations.DeleteModel(
            name='Transactions',
        ),
    ]
