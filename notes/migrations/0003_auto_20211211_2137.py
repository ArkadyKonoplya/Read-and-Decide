# Generated by Django 3.2.9 on 2021-12-12 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_alter_providernote_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providernote',
            name='session_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='providernote',
            name='session_time',
            field=models.TimeField(null=True),
        ),
    ]
