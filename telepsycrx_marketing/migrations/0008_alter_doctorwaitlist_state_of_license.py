# Generated by Django 3.2.9 on 2022-02-15 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20220214_1610'),
        ('telepsycrx_marketing', '0007_usersuggestion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorwaitlist',
            name='state_of_license',
            field=models.ManyToManyField(related_name='license_state', to='accounts.Doctor'),
        ),
    ]