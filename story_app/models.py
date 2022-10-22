from django.db import models
from taggit.managers import TaggableManager
from hitcount.models import HitCountMixin, HitCount
from taggit.models import Tag
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.fields import GenericRelation
import misaka
from django_bleach.models import BleachField
from bs4 import BeautifulSoup
import math

from django.utils.timezone import now

# Create your models here.
class Story(models.Model):
    author_id = models.ForeignKey(
                                    settings.AUTH_USER_MODEL, 
                                    null=True,
                                    default=None, 
                                    on_delete=models.CASCADE
                                )
    title = models.TextField(max_length=300, default='Title')
    content = BleachField(max_length=12000, default='Tell your story.')
    content_html = models.TextField(editable=False, default='')
    content_minified = models.CharField(max_length=12000, editable=False, default='')
    tags = TaggableManager()
    slug = models.SlugField(max_length=601, null=False)
    editable = models.BooleanField(default=False)
    updated = models.BooleanField(default=False)
    published_date = models.DateTimeField(default=now)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
     related_query_name='hit_count_generic_relation')
    cover_image = models.ImageField(upload_to="story_images", default='')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_by', blank=True)
    like_count = models.BigIntegerField(default=0)

    def __str__(self):
        return self.title

    def show_time_since(self):
        user_now = now()
        
        diff = user_now - self.published_date

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "second ago"
            
            else:
                return str(seconds) + " seconds ago"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('detailed_story', kwargs={'author_id':self.author_id, 'pk' : self.pk, 'slug':self.slug})
    
    def save(self, *args, **kwargs):
        
        self.slug = slugify(self.title)
        
        self.content_html = misaka.html(self.content)

        soup = BeautifulSoup(self.content, 'html.parser')
        self.content_minified = soup.get_text()

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
    description = models.TextField(max_length=1200, default='list description')
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

    