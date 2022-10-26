from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from . import models as story_models
from django.forms import ModelForm


class StoryCreateForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
                'class': 'editor__title',
                'oninput':'this.style.height = "";this.style.height = this.scrollHeight + "px";',
                'maxlength':'80',
                
        })
        self.fields['content'].widget.attrs.update({
                'class': 'editor__content', 
                'name':'text',
                'maxlength':'14000'
        })
        self.fields['tags'].widget.attrs.update({
            'class':'editor__tags',
        })
    class Meta:
        model = story_models.Story
        fields = ['title','content','tags', 'cover_image']



class StoryUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
                'class': 'editor__title',
                'oninput':'this.style.height = "";this.style.height = this.scrollHeight + "px";',
                'maxlength':'80',
        })
        self.fields['content'].widget.attrs.update({
                'class': 'editor__content', 
                'name':'text',
                'maxlength':'14000'
        })
        self.fields['tags'].widget.attrs.update({
            'class':'editor__tags',
        })
        
    class Meta:
        model = story_models.Story
        fields = ['title','content','tags', 'cover_image']

class ListUpdateForm(ModelForm):
    class Meta:
        model = story_models.StoryList
        fields = ['name','description']
