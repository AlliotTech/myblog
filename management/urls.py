from django.urls import path
from . import views

app_name = "management"

urlpatterns = [
    path('management', views.management, name='management'),
    # 后台管理模块
    path('dashboard/', views.dashboard, name='dashboard'),
    # 后台管理dashboard
    path('articleAdd/', views.articleAdd, name='articleAdd'),
    # 新增文章
    path('articleList/', views.articleList, name='articleList'),
    # 文章列表
    path('articleCategory/', views.articleCategory, name='articleCategory'),
    # 文章分类
    path('articleTag/', views.articleTag, name='articleTag'),
    # 文章标签
    path('articleComment/', views.articleComment, name='articleComment'),
    # 文章评论
    path('websiteLeaveMessage/', views.websiteLeaveMessage, name='websiteLeaveMessage'),
    # 网站留言
    path('websiteCarousel/', views.websiteCarousel, name='websiteCarousel'),
    # 网站轮播图
    path('websiteLink/', views.websiteLink, name='websiteLink'),
    # 网站友情链接
    path('managementUser/', views.managementUser, name='managementUser'),
    # 用户管理

    path('coverUpload/', views.coverUpload, name='coverUpload'),
    # ajax文章封面图片上传
    path('articleDel/', views.articleDel, name='articleDel'),
    # ajax删除文章
    path('articleEdit-<int:article_id>/', views.articleEdit, name='articleEdit'),
    # ajax修改文章
    path('categoryDel/', views.categoryDel, name='categoryDel'),
    # ajax删除分类
    path('categoryEdit/', views.categoryEdit, name='categoryEdit'),
    # ajax修改分类
    path('categoryAdd/', views.categoryAdd, name='categoryAdd'),
    # ajax新增分类

]
