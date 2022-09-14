from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from . import models as author_models
from story_app import models as story_models

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        author_models.UserExtra.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_starter_list(sender, instance, created, **kwargs):
    if created:
        story_models.StoryList.objects.create(user=instance, name='Reading List')