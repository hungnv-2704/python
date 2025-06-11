from rest_framework import viewsets
from .models import User, Article, Tag
from .serializers import UserSerializer, ArticleSerializer, TagSerializer, ProfileSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().select_related('author').prefetch_related('tags')
    serializer_class = ArticleSerializer
    lookup_field = 'id' 
class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'username'
