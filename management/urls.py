from django.urls import path
from . import views

app_name = "management"

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    # 后台管理dashboard
    path('articleAdd/', views.articleAdd, name='articleAdd'),
    # 新增文章
    path('articleList/', views.articleList, name='articleList'),
    # 文章列表
    path('articleClass/', views.articleClass, name='articleClass'),
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
]
