from rest_framework import serializers
from .models import NewsTag, Article
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class NewsTagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NewsTag
        fields = ['id', 'title']

class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = NewsTagSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'excerpt', 'author', 
            'tags', 'published_at', 'created_at', 'updated_at',
            'status', 'status_display', 'is_featured', 'views_count'
        ]
        read_only_fields = ['views_count']