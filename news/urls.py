from rest_framework.routers import SimpleRouter
from news.views import (
    NewsTagViewSet,
    ArticleViewSet
)

router = SimpleRouter()
router.register(r'news-tags', NewsTagViewSet)
router.register(r'news-articles', ArticleViewSet)