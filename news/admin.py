from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
# Register your models here.
from .models import *


@admin.register(NewsTag)
class NewsTagAdmin(ModelAdmin):
    pass

@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    pass
