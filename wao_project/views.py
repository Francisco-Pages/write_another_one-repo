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


class HomePage(TemplateView):
    template_name = 'index.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user_extra'] = author_models.UserExtra.objects.select_related('user')
        context['stories'] = story_models.Story.objects.select_related('author_id').order_by('-published_date')    
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('author:author_home')
        return super(project_views.HomePage, self).dispatch(request, *args, **kwargs)

