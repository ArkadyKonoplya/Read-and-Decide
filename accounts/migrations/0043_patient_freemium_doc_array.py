# Generated by Django 3.2.9 on 2022-04-26 00:07

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0042_auto_20220425_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='freemium_doc_array',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, default=list, null=True, size=None),
        ),
    ]