from rest_framework import viewsets
from .models import User, Article, Tag
from .serializers import UserSerializer, ArticleSerializer, TagSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().select_related('author').prefetch_related('tags')
    serializer_class = ArticleSerializer

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
