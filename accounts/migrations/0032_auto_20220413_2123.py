# Generated by Django 3.2.9 on 2022-04-14 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_auto_20220413_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='height_ft',
            field=models.IntegerField(default=0, max_length=2),
        ),
        migrations.AlterField(
            model_name='patient',
            name='height_inch',
            field=models.IntegerField(default=0, max_length=2),
        ),
    ]
