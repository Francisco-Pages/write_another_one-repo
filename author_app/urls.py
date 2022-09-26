from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'author_app'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="author_app/login.html"),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('<slug>/<pk>/', views.AuthorDetailView.as_view(), name="detailed_author"),
    # path('author/', views.AuthorTemplateView.as_view(), name="author"),
    path('home/', views.AuthorHomePageView.as_view(), name='author_home'),
    # path('home/<username>/<pk>', views.AuthorHomePageView.as_view(), name='author_home'),
    path('update/<slug>/<pk>/', views.UserExtraUpdateView.as_view(), name='update-user-extra'), 
    path('follow-author/', views.follow_author, name="follow_author"),
]
