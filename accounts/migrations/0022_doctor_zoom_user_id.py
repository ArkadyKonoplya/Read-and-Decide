# Generated by Django 3.2.9 on 2022-04-05 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_merge_20220402_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='zoom_user_id',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
