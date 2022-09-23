from django.db import models
from taggit.managers import TaggableManager
from hitcount.models import HitCountMixin, HitCount
from taggit.models import Tag
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.fields import GenericRelation
import misaka

from django.utils.timezone import now

# Create your models here.
class Story(models.Model):
    author_id = models.ForeignKey(
                                    settings.AUTH_USER_MODEL, 
                                    null=True,
                                    default=None, 
                                    on_delete=models.CASCADE
                                )
    title = models.CharField(max_length=300, default='title')
    content = models.TextField(max_length=12000, default='story')
    content_html = models.TextField(editable=False, default='Tell your story.')
    tags = TaggableManager()
    slug = models.SlugField(null=False)
    editable = models.BooleanField(default=False)
    updated = models.BooleanField(default=False)
    published_date = models.DateTimeField(default=now)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
     related_query_name='hit_count_generic_relation')
    cover_image = models.ImageField(upload_to="static/media/story_images", default='none')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_by', blank=True)
    like_count = models.BigIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('detailed_story', kwargs={'author_id':self.author_id, 'pk' : self.pk, 'slug':self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.content_html = misaka.html(self.content)
        return super().save(*args, **kwargs)


                                
class EditSuggestion(models.Model):
    editor_id = models.ForeignKey(
                                    settings.AUTH_USER_MODEL,
                                    null=True,
                                    default=None,
                                    on_delete=models.CASCADE
                                )    
    story_id = models.ForeignKey(
                                    Story, 
                                    default=None,
                                    on_delete=models.CASCADE
                                )
    content_removed = models.CharField(max_length=12000, default='content removed')
    content_added = models.CharField(max_length=12000, default='content added')
    comments = models.CharField(max_length=12000, default='comments')
    liked = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=now)

class UpdatedStory(models.Model):
    og_story_id = models.ForeignKey(
                                    Story, 
                                    default=None,
                                    on_delete=models.CASCADE
                                )
    new_title = models.CharField(max_length=300, default='new title')
    new_content = models.CharField(max_length=12000, default='new content')
    created_date = models.DateTimeField(default=now)

class StoryList(models.Model):
    user = models.ForeignKey(
                            settings.AUTH_USER_MODEL,
                            related_name='owner',
                            null=True,
                            default=None,
                            on_delete=models.CASCADE
                        )    
    slug = models.SlugField(allow_unicode=True, default='slug')
    name = models.CharField(max_length=300, default='list name')
    description = models.CharField(max_length=1200, default='list description')
    stories = models.ManyToManyField(Story)
    pinners = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='pinned_by', blank=True)
    pinner_count = models.BigIntegerField(default='0')
    created_date = models.DateTimeField(default=now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse(
            "author-list",
            kwargs={
                "owner": self.user.username,
                "slug": self.slug,
                "pk": self.pk,
            }
        )

    class Meta:
        ordering = ['created_date']
    

class LikedStory(models.Model):
    user = models.ForeignKey(
                                settings.AUTH_USER_MODEL,
                                null=True,
                                default=None,
                                on_delete=models.CASCADE
                            )
    story = models.ForeignKey(
                                Story, 
                                default=None,
                                on_delete=models.CASCADE
                            )
    liked_date = models.DateTimeField(default=now)

class TagsExtra(models.Model):
    tag = models.OneToOneField(Tag,
                                default=None,
                                on_delete=models.CASCADE,
                                primary_key=True
                            )
    follower_count = models.BigIntegerField(default='0')
    story_count = models.BigIntegerField(default='0')
    description = models.CharField(max_length=300, default='')
    date_created = models.DateTimeField(default=now)

    