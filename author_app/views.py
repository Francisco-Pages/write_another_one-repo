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
        current_user = get_object_or_404(
            author_models.UserExtra, user=request.user)

        if author.followers.filter(pk=request.user.pk).exists():
            author.followers.remove(request.user)
            current_user.following.remove(author.user.pk)
            author.follower_count -= 1
            current_user.following_count -= 1
            result = author.follower_count
            followed = 'follow'
            author.save()
            current_user.save()
        else:
            author.followers.add(request.user)
            current_user.following.add(author.user.pk)
            author.follower_count += 1
            current_user.following_count += 1
            result = author.follower_count
            followed = 'following'
            author.save()
            current_user.save()
        return JsonResponse({'result': result, 'followed': followed})


# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("author:author_home")
    template_name = "author_app/signup.html"


class UserExtraUpdateView(LoginRequiredMixin, UpdateView):
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
        current_user = author_models.UserExtra.objects.get(
            user=self.request.user)
        context['current_user'] = current_user
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('author:detailed_author', kwargs={'slug': self.object.user, 'pk': self.object.user.pk})


class AuthorDetailView(DetailView):
    login_url = reverse_lazy('login')
    model = authmodels.User
    template_name = "detailed_author.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_extra = author_models.UserExtra.objects.get(user=self.object)
        stories_by_user = [
            story for story in object_extra.stories.all().order_by('-published_date')]
        if self.request.user.is_authenticated:
            current_user = author_models.UserExtra.objects.get(
                user=self.request.user)
            context['current_user'] = current_user
        context['object_extra'] = object_extra
        context['stories'] = stories_by_user
        return context


class AuthorHomePageView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'author_home.html'
    # model = author_models.UserExtra

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_user = author_models.UserExtra.objects.get(
            user=self.request.user)
        following_users = [user for user in author_models.UserExtra.objects.select_related(
            'user') if user.user in current_user.following.all()]
        following_user_ids = [user.user for user in author_models.UserExtra.objects.select_related(
            'user') if user.user in current_user.following.all()]
        feed_stories = story_models.Story.objects.filter(Q(author_id__in=current_user.following.all()) | Q(
            author_id=self.request.user)).order_by('-published_date')

        context["current_user"] = current_user
        context['user_extra'] = following_users
        context['following_stories'] = feed_stories

        return context
