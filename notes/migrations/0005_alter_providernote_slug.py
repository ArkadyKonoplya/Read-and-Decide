# Generated by Django 3.2.9 on 2021-12-12 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_alter_providernote_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providernote',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, null=True),
        ),
    ]
