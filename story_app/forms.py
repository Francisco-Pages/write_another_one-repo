from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from . import models as story_models
from django.forms import ModelForm




class StoryUpdateForm(ModelForm):
    class Meta:
        model = story_models.Story
        fields = ['title','content','tags', 'cover_image']

class ListUpdateForm(ModelForm):
    class Meta:
        model = story_models.StoryList
        fields = ['name','description']
