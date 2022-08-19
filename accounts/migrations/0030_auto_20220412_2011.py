# Generated by Django 3.2.9 on 2022-04-13 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_auto_20220410_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='duration',
            field=models.IntegerField(choices=[], default=30),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='office_is_active',
            field=models.BooleanField(default=True),
        ),
    ]