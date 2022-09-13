from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.Story)
admin.site.register(models.EditSuggestion)
admin.site.register(models.UpdatedStory)
admin.site.register(models.StoryList)
# admin.site.register(models.ListedStory)

admin.site.register(models.LikedStory)
admin.site.register(models.TagsFollowed)