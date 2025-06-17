from rest_framework import serializers, generics
from rest_framework.validators import UniqueValidator
from .models import User, Article, Comment, Tag

class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

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
        read_only_fields = ['created_at', 'updated_at', 'author', 'favorited_by']
        
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
