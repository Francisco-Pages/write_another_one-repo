# Generated by Django 4.1.1 on 2022-10-22 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story_app', '0048_alter_story_content_html_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='slug',
            field=models.SlugField(max_length=601),
        ),
    ]
