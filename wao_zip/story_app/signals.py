from django.db.models.signals import post_save, post_delete, pre_delete, m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver
from . import models as story_models
from author_app import models as author_models
from taggit.models import Tag, TaggedItem

# @receiver(m2m_changed, sender=story_models.Story)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         created_story = story_models.Story.objects.get(id=instance.id)
#         author_models.UserExtra.stories.add(created_story)

@receiver(post_save, sender=Tag)
def create_profile(sender, instance, created, **kwargs):
    if created:
        created_tag = Tag.objects.get(pk=instance.pk)
        story_models.TagsExtra.objects.create(pk=created_tag.pk)

@receiver(post_save, sender=TaggedItem)
def create_tag_extra_story(sender, instance, created, **kwargs):
    if created:
        selected = story_models.TagsExtra.objects.get(pk=instance.tag)
        selected.story_count += 1
        selected.save()

@receiver(post_delete, sender=TaggedItem)
def delete_tag_extra_story(sender, instance, **kwargs):
    selected = story_models.TagsExtra.objects.get(pk=instance.tag)
    selected.story_count -= 1
    selected.save()
