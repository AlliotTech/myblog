from django.contrib import admin
from .models import UserInfo
# Register your models here.


# 用户详细信息
@admin.register(UserInfo)
class ArticleAdmin(admin.ModelAdmin):
    def sexShow(self):
        print(type(self.sex))
        if int(self.sex):
            return "女"
        else:
            return "男"

    sexShow.short_description = "性别"
    list_display = ('id', 'user', 'phone', sexShow, 'aboutme', 'photo')
    # 文章列表里显示想要显示的字段
    list_display_links = ('id', 'phone')
    # 设置哪些字段可以点击进入编辑界面

