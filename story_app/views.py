from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, CreateView, ListView, TemplateView, UpdateView
from hitcount.views import HitCountDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.http import Http404, HttpResponseRedirect, JsonResponse
from taggit.models import Tag
from django.db.models import Q, F
from . import forms



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


def follow_tag(request):
    if request.POST.get('action') == 'post':
        result = ''
        followed = ''
        pk = int(request.POST.get('tagpk'))
        tag = get_object_or_404(Tag, pk=pk)
        tag_counter = get_object_or_404(story_models.TagsFollowed, pk=pk)
        current_user = get_object_or_404(author_models.UserExtra, user=request.user)

        if current_user.tags.filter(pk=pk).exists():
            current_user.tags.remove(pk)
            tag_counter.follower_count -= 1
            result = tag_counter.follower_count
            followed = "Follow"
            tag_counter.save()
        else:
            current_user.tags.add(pk)
            tag_counter.follower_count += 1
            result = tag_counter.follower_count
            followed = "Following"
            tag_counter.save()
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


class StoryDetailView(LoginRequiredMixin, HitCountDetailView):
    login_url = reverse_lazy('login')
    model = story_models.Story
    template_name = "detailed_story.html"
    count_hit = True

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_extras = author_models.UserExtra.objects.get(user=self.object.author_id)
        current_user = author_models.UserExtra.objects.get(user=self.request.user)
        context['user_extras'] = user_extras
        context['current_user'] = current_user
        context.update({'popular_posts': story_models.Story.objects.order_by('-hit_count_generic__hits')[:3],})
        return context
    


class WriteStoryCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    success_url = reverse_lazy("home")
    template_name = "write.html"

    model = story_models.Story
    fields = ['title', 'content', 'tags', 'cover_image']

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
        print(self.object.tags)
        # tags = self.object.tags
        # for tag in tags:
        #     tag_extra = story_models.TagsFollowed.objects.filter(pk=tag.pk).exists()
        #     if tag_extra:
        #         existing_tag = story_models.objects.get(pk=tag.pk)
        #         existing_tag.follower_count += 1
        #         existing_tag.save()
        #     else:
        #         new_tag = story_models.TagsFollowed.objects.create(pk=tag.pk, follower_count=1)
        #         new_tag.save()

        return super().form_valid(form)
    
class StoryUpdateView(LoginRequiredMixin, UpdateView):
    model = story_models.Story
    form_class = forms.StoryUpdateForm
    # success_url = reverse_lazy("detailed_author")
    template_name = 'write.html'

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
        self.user_lists = story_models.StoryList.objects.all().select_related('user')
        return [user_list for user_list in self.user_lists if user_list.user == self.request.user]

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
        context['current_user'] = current_user
        context['user_extras'] = user_extras
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
        tag_extra = story_models.TagsFollowed.objects.get(pk=self.object.pk)
        context['tag_extra'] = tag_extra
        context['current_user'] = current_user
        return context

class StorySearchResultsView(LoginRequiredMixin, ListView):
    model = story_models.Story
    template_name = 'story_search_results.html'
    login_url = reverse_lazy('login')

    extra_context = {
        'user_extras': author_models.UserExtra.objects.all().select_related('user'),
    }

    def get_queryset(self):  
        query = self.request.GET.get("q")
        object_list = story_models.Story.objects.order_by('-published_date').filter(~Q(author_id=self.request.user)).filter(
            Q(content__icontains=query)
        )
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = author_models.UserExtra.objects.get(user=self.request.user)
        query = self.request.GET.get("q")
        context['current_user'] = current_user
        context['query'] = query
        return context
        

class AuthorSearchResultsView(LoginRequiredMixin, ListView):
    model = author_models.UserExtra
    template_name = 'author_search_results.html'
    login_url = reverse_lazy('login')

    def get_queryset(self):  
        query = self.request.GET.get("q")
        object_list = author_models.UserExtra.objects.filter(~Q(user=self.request.user)).filter(
            Q(user__username__icontains=query)
        )
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q")
        current_user = author_models.UserExtra.objects.get(user=self.request.user)
        context['query'] = query
        context['current_user'] = current_user
        return context


    
class SearchPageView(LoginRequiredMixin,TemplateView):
    template_name = 'story_search_results.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = author_models.UserExtra.objects.get(user=self.request.user)
        context['current_user'] = current_user
        return context