from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.serializers import ProfileRetrieveAPIView
# from .views import UserViewSet, ArticleViewSet, TagViewSet, ProfileViewSet, RegisterView, LoginView, UserUpdateView
from .views import RegisterView, UserUpdateView, LoginView, UserRetrieveView, ArticleListAPIView, ArticleFeedAPIView, ArticleFavoriteAPIView

# router = DefaultRouter()
# router.register(r'users', UserViewSet, basename='user')
# router.register(r'articles', ArticleViewSet, basename='article')
# router.register(r'tags', TagViewSet, basename='tag')
# router.register(r'profiles', ProfileViewSet, basename='profile')
# router.register(r'users/register', RegisterView, basename='register')
# router.register(r'users/edit', UserUpdateView, basename='update')
# router.register(r'users/login', LoginView, basename='login')
# Removed duplicate registration for article-detail

urlpatterns = [
    # path('users', UserViewSet.as_view(), name='user'),
    # path('', include(router.urls)),
    path('users/register', RegisterView.as_view(), name='register'),  # Explicitly define RegisterView
    path('users/edit', UserUpdateView.as_view(), name='update'),      # Explicitly define UserUpdateView
    path('users/login', LoginView.as_view(), name='login'),
    path('users', UserRetrieveView.as_view(), name='login'),
    path('articles', ArticleListAPIView.as_view(), name='article-list'),
    path('articles/feed', ArticleFeedAPIView.as_view(), name='article-feed'),
    path('aarticles/<slug:slug>/favorite', ArticleFavoriteAPIView.as_view(), name='article-favorite'),
]
