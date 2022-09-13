from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from story_app import models as story_models
from author_app import models as author_models
from author_app import views as author_views
from . import views as project_views
from taggit.models import Tag


class TestPage(TemplateView):
    template_name = 'test.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

class HomePage(TemplateView):
    template_name = 'index.html'
    
    
    extra_context={
        'stories': story_models.Story.objects.select_related('author_id'),
        # 'tags_followed': story_models.TagsFollowed.objects.all(),
    }

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('author:author_home')
            # return redirect('author:author_home', username=request.user.username, pk=request.user.pk)
        return super(project_views.HomePage, self).dispatch(request, *args, **kwargs)




    # def get(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return HttpResponseRedirect(reverse("test"))
    #     return super().get(request, *args, **kwargs) 
