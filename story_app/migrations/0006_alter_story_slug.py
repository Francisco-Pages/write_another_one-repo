# Generated by Django 4.0.3 on 2022-08-31 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story_app', '0005_story_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='slug',
            field=models.SlugField(),
        ),
    ]
