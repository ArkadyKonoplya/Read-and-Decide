# Generated by Django 3.2.9 on 2022-04-04 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_auto_20220402_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='board_certified_speciality',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
