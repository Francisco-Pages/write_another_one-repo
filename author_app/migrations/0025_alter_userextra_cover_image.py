# Generated by Django 4.0.3 on 2022-09-28 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author_app', '0024_alter_userextra_about_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextra',
            name='cover_image',
            field=models.ImageField(default='', upload_to='author_images'),
        ),
    ]
