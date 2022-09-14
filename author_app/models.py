from django.db import models
from django.contrib.auth import models as authmodels
from django.utils import timezone
from django.conf import settings
from taggit.models import Tag


from story_app import models as story_models

from django.utils.timezone import now

# Create your models here.
class User(authmodels.User, authmodels.PermissionsMixin):

    def __str__(self):
        return self.username

    
class UserExtra(models.Model):
    user = models.OneToOneField(
                            settings.AUTH_USER_MODEL,
                            default=None, 
                            on_delete=models.CASCADE
                        )
    about_user = models.CharField(max_length=300, default='About author')
    cover_image = models.ImageField(upload_to="static/media/author_images", default='static/svg/profile-icon.svg')
    stories = models.ManyToManyField(story_models.Story)
    lists = models.ManyToManyField(story_models.StoryList)
    following_tags = models.ManyToManyField(Tag)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followers')
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following')




    def __str__(self):
        return self.user.username

    # def get_absolute_url(self):
    #     return reverse(
    #         "author_home",
    #         kwargs={
    #             "username": self.user.username,
    #             "pk": self.user.pk,
    #         }
    #     )

    class Meta:
        db_table = 'user_extra'
        constraints = [
            models.UniqueConstraint(fields=['user',], name='unique_user_profile')
        ]


class Follow(models.Model):
    follower_id = models.ForeignKey(
                                    settings.AUTH_USER_MODEL,
                                    null=True,
                                    default=None,
                                    related_name="user_follower",
                                    on_delete=models.CASCADE
                                )
    following_id = models.ForeignKey(
                                    settings.AUTH_USER_MODEL,
                                    null=True,
                                    default=None,
                                    related_name="user_following",
                                    on_delete=models.CASCADE
                                )
    followed_date = models.DateField(default=now)

    class Meta:
        db_table = 'follow'
        constraints = [
            models.UniqueConstraint(fields=['follower_id', 'following_id'], name='unique_follow')
        ]

    

    
    
class Message(models.Model):
    sender_id = models.ForeignKey(
                                    settings.AUTH_USER_MODEL,
                                    null=True,
                                    default=None,
                                    related_name="sender",
                                    on_delete=models.CASCADE
                                )
    receiver_id = models.ForeignKey(
                                    settings.AUTH_USER_MODEL,
                                    null=True,
                                    default=None,
                                    related_name="receiver",
                                    on_delete=models.CASCADE
                                )
    title = models.CharField(max_length=300, default='Message Title')
    content = models.CharField(max_length=1200, default='Message Content')
    read = models.BooleanField(default=False)
    sent_date = models.DateField(default=now)

    def __str__(self):
        return f"from: {self.sender_id}, to: {self.receiver_id}"







