from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Chengyu

#Blog模型的管理器
@admin.register(Chengyu)
class ArticleAdmin(admin.ModelAdmin):
    list_display=('id', 'word', 'meaning')
