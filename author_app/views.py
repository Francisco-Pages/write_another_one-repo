from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, DetailView, ListView, UpdateView
from django.contrib.auth import get_user_model
from django.db.models import Q
from time import time
from django.http import JsonResponse
from django.core import serializers

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from story_app import models as story_models
from author_app import models as author_models

from django.contrib.auth import models as authmodels



from . import forms

@login_required
def follow_author(request):
    if request.POST.get('action') == 'post':
        result = ''
        followed = ''
        pk = int(request.POST.get('authorpk'))
        author = get_object_or_404(author_models.UserExtra, pk=pk)
        current_user = get_object_or_404(author_models.UserExtra, user=request.user)

        if author.followers.filter(pk=request.user.pk).exists():
            author.followers.remove(request.user)
            current_user.following.remove(author.user.pk)
            author.follower_count -= 1
            result = author.follower_count
            followed = 'follow'
            author.save()
        else:
            author.followers.add(request.user)
            current_user.following.add(author.user.pk)
            author.follower_count += 1
            result = author.follower_count
            followed = 'following'
            author.save()

        return JsonResponse({'result':result, 'followed':followed})


# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "author_app/signup.html"

class UserExtraUpdateView(UpdateView):
    model = author_models.UserExtra
    form_class = forms.UserExtraUpdateForm
    # success_url = reverse_lazy("home")
    template_name = 'author_app/user_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        handler = super().dispatch(request, *args, **kwargs)
        user = request.user
        user_extra = self.get_object()
        
        if not (user_extra.user == user or user.is_superuser):
            raise PermissionDenied
        return handler

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = author_models.UserExtra.objects.get(user=self.request.user)
        context['current_user'] = current_user
        return context

    def get_success_url(self, **kwargs):    
        return reverse_lazy('author:detailed_author', kwargs = {'slug':self.object.user, 'pk':self.object.user.pk})     
    


class AuthorTemplateView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'author.html'
    
    extra_context = {
        'stories': story_models.Story.objects.all(),
        'follows': author_models.Follow.objects.all(),
    }

# OTHER'S PROFILES
class AuthorDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = authmodels.User
    template_name = "detailed_author.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_extra = author_models.UserExtra.objects.get(user=self.object)
        stories_by_user = [story for story in object_extra.stories.all().order_by('-published_date')]
        current_user = author_models.UserExtra.objects.get(user=self.request.user)
        context['current_user'] = current_user
        context['object_extra'] = object_extra
        context['stories'] = stories_by_user
        return context
    
    
        
    
# OWN PROFILE

class AuthorHomePageView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'author_home.html'
    # model = author_models.UserExtra
        
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_user = author_models.UserExtra.objects.get(user=self.request.user)
        following_users = [user for user in author_models.UserExtra.objects.select_related('user') if user.user in current_user.following.all()]
        following_user_ids = [user.user for user in author_models.UserExtra.objects.select_related('user') if user.user in current_user.following.all()]
        feed_stories = story_models.Story.objects.filter(Q(author_id__in=current_user.following.all()) | Q(author_id= self.request.user)).order_by('-published_date')

        context["current_user"] = current_user
        context['user_extra'] = following_users
        context['following_stories'] = feed_stories
        
        return context

    
        
# class ListsListView(LoginRequiredMixin,ListView):
#     login_url = reverse_lazy('login')
#     template_name = 'story_lists.html'

#     def get_queryset(self, **kwargs):
        
#         self.user_lists = story_models.StoryList.objects.all().select_related('user')

#         return [user_list for user_list in self.user_lists if user_list.user == self.request.user]

# class ListDetailView(LoginRequiredMixin, DetailView):
#     login_url = reverse_lazy('login')
#     model = story_models.StoryList
#     template_name = 'detailed_list.html'


    
    # def get_queryset(self, **kwargs):
        
    #     self.following_stories = story_models.Story.objects.all().select_related('author_id')

    #     return [story for story in self.following_stories if story.author_id == self.request.user]

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["following_stories"] = self.following_stories
    #     return context
    

    # extra_context = {
    #     'stories': story_models.Story.objects.filter().order_by('-published_date'),
    #     'tags_followed': story_models.TagsFollowed.objects.all(),
    #     'authors_followed': author_models.Follow.objects.filter().order_by('-followed_date'),
    #     'user_extras': author_models.UserExtra.objects.all(),

    #     # 'authors_followed': [u for u in author_models.Follow.objects.all()]
    # }

