from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.serializers import ProfileRetrieveAPIView
from .views import UserViewSet, ArticleViewSet, TagViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'profiles', ProfileViewSet, basename='profile')
# Removed duplicate registration for article-detail

urlpatterns = [
    path('', include(router.urls)),
]
