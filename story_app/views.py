from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, CreateView, ListView, TemplateView, UpdateView, DeleteView
from hitcount.views import HitCountDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.core.exceptions import PermissionDenied
from taggit.models import Tag
from django.db.models import Q, F
from . import forms
import datetime



from . import models as story_models
from author_app import models as author_models

from django.contrib.auth import get_user_model
User = get_user_model()

from django.conf import settings


# Create your views here.

def write(request):
    return render(request, 'write.html')

def read(request):
    return render(request, 'read.html')

def test_home(request):
    return render(request, 'story_app/test_home.html')
    
def lists(request):
    return render(request, 'lists.html')

def detailed_list(request):
    return render(request, 'detailed_list.html')

def explore(request):
    return render(request, 'explore.html')


def add_story_to_list(request):
    if request.POST.get('action') =='post':
        added = ''
        added_in_list = ''
        story_pk = int(request.POST.get('storypk'))
        list_pk = int(request.POST.get('listpk'))
        story = get_object_or_404(story_models.Story, pk=story_pk)
        current_user = get_object_or_404(author_models.UserExtra, user=request.user)
        list_obj = get_object_or_404(current_user.lists.all(), pk=list_pk)

        
        if list_obj.stories.filter(pk=story.pk).exists():
            list_obj.stories.remove(story.pk)
            added = "/static/svg/check-box-icon.svg"
            added_in_list = "/static/svg/add-item-icon.svg"
            list_obj.save()
        
        else:
            list_obj.stories.add(story.pk)
            added = "/static/svg/check-box-icon-filled.svg"
            added_in_list = "/static/svg/remove-item-icon.svg"
            list_obj.save()
        
        
        return JsonResponse({'added':added, 'added_in_list':added_in_list})

class RecommendationsFeedView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'recommendations_feed.html'
    # model = author_models.UserExtra
        
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_user = author_models.UserExtra.objects.get(user=self.request.user)
        following_users = [user for user in author_models.UserExtra.objects.select_related('user') if user.user in current_user.following.all()]
        
        tags_stories = []
        for story in story_models.Story.objects.select_related('author_id').order_by('-published_date'):
            for tag in current_user.tags.all():
                if tag in story.tags.all():
                    tags_stories.append(story)
                    break
                

        context['tags_stories'] = tags_stories
        context["current_user"] = current_user
        context['user_extra'] = following_users
        
        return context

def follow_tag(request):
    if request.POST.get('action') == 'post':
        result = ''
        followed = ''
        pk = int(request.POST.get('tagpk'))
        tag = get_object_or_404(Tag, pk=pk)
        tag_counter = get_object_or_404(story_models.TagsExtra, pk=pk)
        current_user = get_object_or_404(author_models.UserExtra, user=request.user)

        if current_user.tags.filter(pk=pk).exists():
            current_user.tags.remove(pk)
            tag_counter.follower_count -= 1
            result = tag_counter.follower_count
            followed = "Follow"
            tag_counter.save()
            current_user.save()
        else:
            current_user.tags.add(pk)
            tag_counter.follower_count += 1
            result = tag_counter.follower_count
            followed = "Following"
            tag_counter.save()
            current_user.save()
        
        return JsonResponse({'result':result, 'followed':followed})



@login_required
def pin_list(request):
    if request.POST.get('action') == 'post':
        result = ''
        pinned = ''
        pk = int(request.POST.get('listpk'))
        list_obj = get_object_or_404(story_models.StoryList, pk=pk)
        current_user = get_object_or_404(author_models.UserExtra, user=request.user)

        if list_obj.pinners.filter(pk=request.user.pk).exists():
            list_obj.pinners.remove(request.user)
            current_user.pinned_lists.remove(list_obj)
            list_obj.pinner_count -= 1
            result = list_obj.pinner_count
            pinned = '/static/svg/add-to-list-icon.svg'
            list_obj.save()
        else:
            list_obj.pinners.add(request.user)
            current_user.pinned_lists.add(list_obj)
            list_obj.pinner_count += 1
            result = list_obj.pinner_count
            pinned = '/static/svg/in-list-icon.svg'
            list_obj.save()
        return JsonResponse({'result':result, 'pinned':pinned})


@login_required
def like_story(request):
    if request.POST.get('action') =='post':
        result = ''
        liked = ''
        pk = int(request.POST.get('storypk'))
        story = get_object_or_404(story_models.Story, pk=pk)
        
        if story.likes.filter(pk=request.user.pk).exists():
            story.likes.remove(request.user)
            story.like_count -= 1
            result = story.like_count
            liked = "/static/svg/like-icon.svg"
            story.save()
        else:
            story.likes.add(request.user)
            story.like_count += 1
            result = story.like_count
            liked = "/static/svg/like-icon-filled.svg"
            story.save()

        return JsonResponse({'result':result, 'liked':liked})


class StoryDetailView(HitCountDetailView):
    login_url = reverse_lazy('login')
    model = story_models.Story
    template_name = "detailed_story.html"
    count_hit = True

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            current_user = author_models.UserExtra.objects.get(user=self.request.user)
            context['current_user'] = current_user

        user_extras = author_models.UserExtra.objects.get(user=self.object.author_id)
        stories_by_author = user_extras.stories.all().exclude(pk=self.object.pk).order_by('-published_date')[:4]
        context['stories_by_author'] = stories_by_author
        context['user_extras'] = user_extras
        # context.update({'popular_posts': story_models.Story.objects.order_by('-hit_count_generic__hits')[:3],})
        return context
    


class WriteStoryCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    success_url = reverse_lazy("home")
    template_name = "write.html"
    form_class = forms.StoryCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = author_models.UserExtra.objects.get(user=self.request.user)
        context['current_user'] = current_user
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author_id = self.request.user
        self.object.save()
        
        user = author_models.UserExtra.objects.get(user=self.request.user)
        user.stories.add(self.object)
        return super().form_valid(form)
    
class StoryUpdateView(LoginRequiredMixin, UpdateView):
    model = story_models.Story
    form_class = forms.StoryUpdateForm
    # success_url = reverse_lazy("detailed_author")
    template_name = 'write.html'

    def dispatch(self, request, *args, **kwargs):
        handler = super().dispatch(request, *args, **kwargs)
        user = request.user
        story = self.get_object()
        
        if not (story.author_id == user or user.is_superuser):
            raise PermissionDenied
        return handler

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = author_models.UserExtra.objects.get(user=self.request.user)
        content_height = len(self.object.content)/1.8
        context['current_user'] = current_user
        context['content_height'] = content_height if content_height > 52 else 52
        
        return context

    def get_success_url(self, **kwargs):    
        return reverse_lazy('author:detailed_author', kwargs = {'slug':self.object.author_id, 'pk':self.object.author_id.pk})     
        
class StoryDeleteView(DeleteView):
    model = story_models.Story 
    template_name = 'story_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        handler = super().dispatch(request, *args, **kwargs)
        user = request.user
        story = self.get_object()
        
        if not (story.author_id == user or user.is_superuser):
            raise PermissionDenied
        return handler

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = author_models.UserExtra.objects.get(user=self.request.user)
        context['current_user'] = current_user
        return context

    def get_success_url(self, **kwargs):    
        return reverse_lazy('author:detailed_author', kwargs = {'slug':self.object.author_id, 'pk':self.object.author_id.pk})     
        


class ListsListView(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('login')
    # model = story_models.StoryList
    template_name = 'story_lists.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = author_models.UserExtra.objects.get(user=self.request.user)
        context['current_user'] = current_user
        return context


    def get_queryset(self, **kwargs):
        self.user_extra = author_models.UserExtra.objects.get(user=self.request.user)
        return [user_list for user_list in self.user_extra.lists.all()]

class ListDeleteView(DeleteView):
    model = story_models.StoryList 
    template_name = 'list_confirm_delete.html'

    def get_success_url(self, **kwargs):    
        return reverse_lazy('story:author-list', kwargs = {'owner':self.request.user.username})     
        

class PinnedListsView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    # model = story_models.StoryList
    template_name = 'pinned_lists.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = author_models.UserExtra.objects.get(user=self.request.user)
        context['current_user'] = current_user
        return context

    def get_queryset(self, **kwargs):
        self.user_lists = author_models.UserExtra.objects.get(user=self.request.user.pk)
        return self.user_lists.pinned_lists.all()

    

class ListCreateView(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('login')
    template_name = 'create_list.html'
    # success_url = reverse_lazy("author-list")
    
    model = story_models.StoryList
    fields = ['name', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = author_models.UserExtra.objects.get(user=self.request.user)
        context['current_user'] = current_user
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        user = author_models.UserExtra.objects.get(user=self.request.user)
        user.lists.add(self.object)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):    
        return reverse_lazy('story:author-list', kwargs = {'owner':self.request.user.username})     


class ListUpdateView(LoginRequiredMixin, UpdateView):
    model = story_models.StoryList
    form_class = forms.ListUpdateForm
    # success_url = reverse_lazy("detailed_author")
    template_name = 'create_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = author_models.UserExtra.objects.get(user=self.request.user)
        context['current_user'] = current_user
        context['update_list'] = self.object.name
        return context

    def get_success_url(self, **kwargs):    
        return reverse_lazy('story:author-list', kwargs = {'owner':self.request.user.username})     
        

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        # user = author_models.UserExtra.objects.get(user=self.request.user)
        # user.stories.add(self.object) -----> create 'lists' field in UserExtra model
        return super().form_valid(form)


class ListDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = story_models.StoryList
    template_name = 'detailed_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = author_models.UserExtra.objects.get(user=self.request.user)
        user_extras = author_models.UserExtra.objects.all().select_related('user') 
        list_owner = author_models.UserExtra.objects.get(user=self.object.user)
        context['current_user'] = current_user
        context['user_extras'] = user_extras
        context['list_owner'] = list_owner
        return context



class TagDetailView(LoginRequiredMixin,DetailView):
    model = Tag
    login_url = reverse_lazy('login')
    template_name = 'detailed_tag.html'

    extra_context = {
        'stories': story_models.Story.objects.all().order_by('-published_date'),
        'user_extras': author_models.UserExtra.objects.all(),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = author_models.UserExtra.objects.get(user=self.request.user)
        tag_extra = story_models.TagsExtra.objects.get(pk=self.object.pk)
        context['tag_extra'] = tag_extra
        context['current_user'] = current_user
        return context

class StorySearchResultsView(LoginRequiredMixin, ListView):
    model = story_models.Story
    template_name = 'story_search_results.html'
    login_url = reverse_lazy('login')

    
    def get_queryset(self):  
        if self.request.GET.get('q') == None:
            query = ''
        else:
            query = self.request.GET.get("q")
        
        object_list = story_models.Story.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) 
        ).order_by('-published_date')
        
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('q') == None:
            query = ''
        else:
            query = self.request.GET.get("q")
        context['user_extras'] = author_models.UserExtra.objects.select_related('user')
        context['current_user'] = author_models.UserExtra.objects.get(user=self.request.user)
        context['query'] = query
        return context
        

class AuthorSearchResultsView(LoginRequiredMixin, ListView):
    model = author_models.UserExtra
    template_name = 'author_search_results.html'
    login_url = reverse_lazy('login')

    def get_queryset(self):  
        if self.request.GET.get('q') == None:
            query = ''
        else:
            query = self.request.GET.get("q")
        
        object_list = author_models.UserExtra.objects.filter(
            Q(user__username__icontains=query) | Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query)
        ).order_by('-follower_count')
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('q') == None:
            query = ''
        else:
            query = self.request.GET.get("q")
        current_user = author_models.UserExtra.objects.get(user=self.request.user)
        context['query'] = query
        context['current_user'] = current_user
        return context

class TagSearchResultsView(LoginRequiredMixin, ListView):
    model = story_models.TagsExtra()
    template_name = 'tag_search_results.html'
    login_url = reverse_lazy('login')

    def get_queryset(self):  
        if self.request.GET.get('q') == None:
            query = ''
        else:
            query = self.request.GET.get("q")
        object_list = story_models.TagsExtra.objects.filter(
            Q(tag__name__icontains=query)
        ).order_by('-follower_count')
        return object_list


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('q') == None:
            query = ''
        else:
            query = self.request.GET.get("q")
        context['query'] = query
        context['current_user'] = author_models.UserExtra.objects.get(user=self.request.user)
        return context
    
    
class SearchPageView(LoginRequiredMixin,TemplateView):
    template_name = 'story_search_results.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = author_models.UserExtra.objects.get(user=self.request.user)
        context['current_user'] = current_user
        return context