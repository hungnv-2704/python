from rest_framework import serializers, generics
from .models import User, Article, Comment, Tag

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'image']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body', 'created_at']

class ArticleCommentListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Comment.objects.filter(article__slug=slug).order_by('-created_at')
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    class Meta:
        model = User
        fields = ['username', 'bio']

class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    lookup_field = 'username'  # Change lookup_field to 'username'
    queryset = User.objects.all()

    def get_queryset(self):
        return User.objects.filter(username=self.kwargs['username'])
