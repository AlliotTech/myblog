from django.contrib import admin
from .models import UserInfo, ArticleViewHistory, LeaveMessage


# Register your models here.


# 用户详细信息
@admin.register(UserInfo)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'sex', 'aboutme', 'web', 'photo')
    # 文章列表里显示想要显示的字段
    list_display_links = ('id', 'sex', 'phone')
    # 设置哪些字段可以点击进入编辑界面


# 用户浏览记录
@admin.register(ArticleViewHistory)
class ArticleViewHistoryAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'time', 'is_like')
    # 文章列表里显示想要显示的字段
    list_display_links = ('article', 'user', 'is_like')
    # 设置哪些字段可以点击进入编辑界面


# 用户留言记录
@admin.register(LeaveMessage)
class LeaveMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'user', 'time', 'level', 'father')
    list_display_links = ('content', 'user')
