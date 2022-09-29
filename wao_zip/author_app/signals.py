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
        created_list = story_models.StoryList.objects.create(user=instance, name='Reading List')
        created_list.save()
        current_user = author_models.UserExtra.objects.get(user=instance)
        current_user.lists.add(created_list)