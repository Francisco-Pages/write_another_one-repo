# Generated by Django 4.1.1 on 2022-10-10 15:25

from django.db import migrations
import django_bleach.models


class Migration(migrations.Migration):

    dependencies = [
        ('story_app', '0044_alter_story_content_html'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='content',
            field=django_bleach.models.BleachField(default='Tell your story.', max_length=12000),
        ),
    ]
