from django.contrib import admin

# Register your models here.
from .models import *



admin.site.register(NewsCategory)
admin.site.register(NewsTag)
admin.site.register(NewsCollection)
admin.site.register(NewsArticle)