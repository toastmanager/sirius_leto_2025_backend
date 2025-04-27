from rest_framework import serializers
from .models import NewsCategory, NewsTag, NewsCollection, NewsArticle
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ['id', 'title']

class NewsTagSerializer(serializers.ModelSerializer):
    category = NewsCategorySerializer(read_only=True)
    
    class Meta:
        model = NewsTag
        fields = ['id', 'title', 'category']

class NewsCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCollection
        fields = ['id', 'title', 'created_at', 'updated_at']

class NewsArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = NewsTagSerializer(many=True, read_only=True)
    collection = NewsCollectionSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = NewsArticle
        fields = [
            'id', 'title', 'content', 'excerpt', 'author', 
            'tags', 'published_at', 'created_at', 'updated_at',
            'collection', 'status', 'status_display', 
            'is_featured', 'views_count'
        ]
        read_only_fields = ['views_count']