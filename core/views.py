from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import User, Article, Tag
from .serializers import UserSerializer, ArticleSerializer, TagSerializer, ProfileSerializer, UserRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginView(TokenObtainPairView):
    # có thể tùy biến serializer_class nếu cần thêm dữ liệu
    pass

# GET /api/user - Lấy thông tin người dùng đã đăng nhập
class UserRetrieveView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data})

# PUT /api/user - Cập nhật thông tin
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'user': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ArticleListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Article.objects.all()

        tag = request.query_params.get('tag')
        author = request.query_params.get('author')

        if tag:
            queryset = queryset.filter(tags__name=tag)
        if author:
            queryset = queryset.filter(author__username=author)

        # Pagination (LimitOffset)
        limit = int(request.query_params.get('limit', 10))
        offset = int(request.query_params.get('offset', 0))
        total = queryset.count()
        queryset = queryset[offset:offset+limit]

        serializer = ArticleSerializer(queryset, many=True, context={'request': request})
        return Response({
            'articles': serializer.data,
            'articlesCount': total
        })
class ArticleFeedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        following_users = user.following.values_list('followed__id', flat=True)
        queryset = Article.objects.filter(author__in=following_users).order_by('-created_at')

        limit = int(request.query_params.get('limit', 10))
        offset = int(request.query_params.get('offset', 0))
        total = queryset.count()
        queryset = queryset[offset:offset+limit]

        serializer = ArticleSerializer(queryset, many=True, context={'request': request})
        return Response({
            'articles': serializer.data,
            'articlesCount': total
        })
class ArticleFavoriteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        article.favorited_by.add(request.user)
        article.save()

        serializer = ArticleSerializer(article, context={'request': request})
        return Response({'article': serializer.data}, status=status.HTTP_200_OK)
# class ArticleViewSet(viewsets.ModelViewSet):
#     queryset = Article.objects.all().select_related('author').prefetch_related('tags')
#     serializer_class = ArticleSerializer
#     lookup_field = 'id' 
# class TagViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer

# class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = ProfileSerializer
#     lookup_field = 'username'
