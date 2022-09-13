from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, ListView, UpdateView
from django.contrib.auth import get_user_model

from django.contrib.auth.mixins import LoginRequiredMixin

from story_app import models as story_models
from author_app import models as author_models

from django.contrib.auth import models as authmodels



from . import forms



# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "author_app/signup.html"

class UserExtraUpdateView(UpdateView):
    model = author_models.UserExtra
    form_class = forms.UserExtraUpdateForm
    success_url = reverse_lazy("home")
    template_name = 'author_app/user_update_form.html'



# @login_required(login_url="/author/login/")
# def author(request):
#     # current_user = request.user
#     return render(request, 'author.html')

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
        following_stories = [story for story in story_models.Story.objects.select_related('author_id').order_by('-published_date') if story.author_id in following_user_ids]
        context["current_user"] = current_user
        context['following_users'] = following_users
        context['following_stories'] = following_stories

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

