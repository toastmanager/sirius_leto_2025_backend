from rest_framework.routers import DefaultRouter
from django.urls import path, include
from news.views import (
    NewsCategoryViewSet,
    NewsTagViewSet,
    NewsCollectionViewSet,
    NewsArticleViewSet
)

router = DefaultRouter()
router.register(r'news-categories', NewsCategoryViewSet)
router.register(r'news-tags', NewsTagViewSet)
router.register(r'news-collections', NewsCollectionViewSet)
router.register(r'news-articles', NewsArticleViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]