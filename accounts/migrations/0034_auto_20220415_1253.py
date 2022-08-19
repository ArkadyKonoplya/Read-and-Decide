# Generated by Django 3.2.9 on 2022-04-15 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0033_auto_20220413_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='height',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='height_unit',
            field=models.CharField(choices=[('ft', 'Ft'), ('cm', 'Cm')], default='ft', max_length=2),
        ),
        migrations.AddField(
            model_name='patient',
            name='weight_unit',
            field=models.CharField(choices=[('lb', 'Lb'), ('kg', 'Kg')], default='lb', max_length=2),
        ),
        migrations.AlterField(
            model_name='patient',
            name='subscription_type',
            field=models.CharField(blank=True, choices=[('Free_Membership', 'Free Membership'), ('Medication_N_CareCounseling', 'Medication N Carecounseling'), ('Medication_Therapy', 'Medication Therapy'), ('Therapy', 'Therapy')], max_length=70, null=True),
        ),
    ]
