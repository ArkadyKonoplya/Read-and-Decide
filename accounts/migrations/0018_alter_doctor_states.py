# Generated by Django 3.2.9 on 2022-03-27 04:02

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20220325_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='states',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=300), blank=True, null=True, size=None),
        ),
    ]