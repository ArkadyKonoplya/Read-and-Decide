# Generated by Django 3.2.9 on 2022-06-10 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0054_auto_20220607_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotatedresponse',
            name='shared_with_doctors',
            field=models.ManyToManyField(blank=True, to='accounts.Doctor'),
        ),
        migrations.AlterField(
            model_name='telepsycrxdownload',
            name='shared_with_doctors',
            field=models.ManyToManyField(blank=True, to='accounts.Doctor'),
        ),
        migrations.AlterField(
            model_name='telepsycrxdownload',
            name='shared_with_patients',
            field=models.ManyToManyField(blank=True, to='accounts.Patient'),
        ),
    ]
