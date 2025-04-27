from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class NewsCategory(models.Model):
    title = models.CharField(max_length=200)
    class Meta:
        verbose_name = ("Категория новостей")
        verbose_name_plural = ("Категория новостей")
    
    def __str__(self):
        return self.title

class NewsTag(models.Model):
    title = models.CharField(max_length=200)
    
    category = models.ForeignKey(
        NewsCategory,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        related_name = 'tags',
        verbose_name=_("Категория")
    )
    class Meta:
        verbose_name = ("Тег новостей")
        verbose_name_plural = ("Теги новостей")
    def __str__(self):
        return self.title

class NewsCollection(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name = "Коллекция новостей"
        verbose_name_plural = "Колекции новостей"

    def __str__(self):
        return self.title
    
class NewsArticle(models.Model):
    STATUS_PUBLISHED = "PUBLISHED"
    STATUS_DRAFT = "DRAFT"
    STATUS_DELETED = 'DELETED'
    STATUS_ARCHIVED = "ARCHIVED"

    STATUS_CHOICES = (
        (STATUS_PUBLISHED, "Опубликовано"),
        (STATUS_DRAFT, "Черновик"),
        (STATUS_DELETED, "Удалено"),
        (STATUS_ARCHIVED, _("В архиве")),
    )
    title = models.CharField(max_length=255, verbose_name=_("Заголовок"))
    content = models.TextField(verbose_name=_("Содержание"))
    excerpt = models.CharField(blank=True,max_length=500,verbose_name=_("Краткое описание"))
    
    autors = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name="news_articles",
        verbose_name=_("Автор")
    )
    
    tags = models.ManyToManyField(
        NewsTag,
        blank=True,
        related_name="articles",
        verbose_name=_("Теги")
    )
    published_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Дата публикации"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))
    collection = models.ForeignKey(
        NewsCollection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
        verbose_name=_("Коллекция")
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        verbose_name=_("Статус")
    )
    is_featured = models.BooleanField(default=False, verbose_name=_("Рекомендуемая новость"))
    views_count = models.PositiveIntegerField(default=0, verbose_name=_("Количество просмотров"))


    class Meta:
        verbose_name = _("Новостная статья")
        verbose_name_plural = _("Новостные статьи")
        ordering = ['-published_at']

    def __str__(self):
        return self.title