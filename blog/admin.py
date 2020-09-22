from django.contrib import admin
from .models import Category, Tag, Article
# 导入需要管理的数据库表
# Register your models here.


# 文章内容
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'view', 'like', 'collection', 'created_time', 'recommend')
    # 文章列表里显示想要显示的字段
    list_per_page = 30
    # 满50条数据就自动分页
    ordering = ('-created_time',)
    # 后台数据列表排序方式
    list_display_links = ('id', 'title')
    # 设置哪些字段可以点击进入编辑界面


# 文章分类
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


# 文章标签
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')





