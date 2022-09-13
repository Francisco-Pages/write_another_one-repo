from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver
from . import models as story_models
from author_app import models as author_models

# @receiver(m2m_changed, sender=story_models.Story)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         created_story = story_models.Story.objects.get(id=instance.id)
#         author_models.UserExtra.stories.add(created_story)

