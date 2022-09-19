from django.urls import path
from . import views

app_name = "story_app"

urlpatterns = [
    # path('new-story', views.write, name='write'),
    # path('read', views.read, name='read'),
    path('test_home', views.test_home, name='test_home'),

    path('read', views.read, name='read'),
    path('write', views.WriteStoryCreateView.as_view(), name='write'),
    path('explore', views.explore, name='explore'),
    path('lists/<owner>/', views.ListsListView.as_view(), name='author-list'),
    path('list/<owner>/<slug>/<pk>/', views.ListDetailView.as_view(), name='detailed_list'),
    path('new-list/', views.ListCreateView.as_view(), name='new-list'),
    path('update-list/<owner>/<slug>/<pk>/', views.ListUpdateView.as_view(), name='update-list'),
    path('story/<author_id>/<slug>/<pk>/', views.StoryDetailView.as_view(), name='detailed_story'),
    path('tag/<slug>/', views.TagDetailView.as_view(), name='detailed-tag'),
    path('search/stories/', views.StorySearchResultsView.as_view(), name='story-search-results'),
    path('search/authors/', views.AuthorSearchResultsView.as_view(), name='author-search-results'),
    path('explore/', views.SearchPageView.as_view(), name='explore'),
    path('update-story/<author_id>/<slug>/<pk>/', views.StoryUpdateView.as_view(), name='update-story'),
    path('like/', views.like_story, name="like_story_ajax"),
    path('pin-list/', views.pin_list, name="pin_list"),

]