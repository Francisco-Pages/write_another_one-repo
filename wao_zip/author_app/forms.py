from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from . import models as author_models
from django.forms import ModelForm


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")
        model = get_user_model()

    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"
        self.fields["email"].required = True

class UserExtraUpdateForm(ModelForm):
    class Meta:
        model = author_models.UserExtra
        fields = ['about_user','cover_image']
