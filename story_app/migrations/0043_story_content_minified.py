# Generated by Django 4.1.1 on 2022-10-07 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story_app', '0042_alter_story_content_alter_story_content_html'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='content_minified',
            field=models.CharField(default='', editable=False, max_length=12000),
        ),
    ]