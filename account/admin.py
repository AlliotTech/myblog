from django.contrib import admin
from .models import UserInfo
# Register your models here.


# 用户详细信息
@admin.register(UserInfo)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'sex', 'aboutme', 'photo')
    # 文章列表里显示想要显示的字段
    list_display_links = ('id', 'phone')
    # 设置哪些字段可以点击进入编辑界面

