# Generated by Django 4.0.3 on 2022-09-20 12:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('story_app', '0027_storylist_pinner_count_alter_storylist_pinners'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tagsfollowed',
            name='user',
        ),
        migrations.AddField(
            model_name='tagsfollowed',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='tag_follower', to=settings.AUTH_USER_MODEL),
        ),
    ]
