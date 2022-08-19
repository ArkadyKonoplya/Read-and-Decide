# Generated by Django 3.2.9 on 2021-12-26 05:41

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0008_auto_20211225_2241'),
        ('telepsycrx_hr', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ApprovedDoctors',
            new_name='ApprovedDoctor',
        ),
        migrations.RenameModel(
            old_name='ApprovedFiles',
            new_name='ApprovedFile',
        ),
        migrations.RenameModel(
            old_name='Uploads',
            new_name='Upload',
        ),
    ]
