from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, UserUpdateView, LoginView, UserRetrieveView, ArticleListAPIView, ArticleFeedAPIView, ArticleFavoriteAPIView, FollowUserAPIView, CommentCreateAPIView

urlpatterns = [
    path('users/register', RegisterView.as_view(), name='register'),
    path('users/edit', UserUpdateView.as_view(), name='update'),
    path('users/login', LoginView.as_view(), name='login'),
    path('users', UserRetrieveView.as_view(), name='login'),
    path('articles', ArticleListAPIView.as_view(), name='article-list'),
    path('articles/feed', ArticleFeedAPIView.as_view(), name='article-feed'),
    path('articles/<slug:slug>/favorite', ArticleFavoriteAPIView.as_view(), name='article-favorite'),
    path('profiles/:username/follow', FollowUserAPIView.as_view(), name='follow-user'),
    path('articles/:slug/comments/:id', CommentCreateAPIView.as_view(), name='article-comment'),
]
