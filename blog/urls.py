from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('media/<str:img_url>', views.compressImage),
    # 图片压缩
    path('category-<int:category_id>/', views.category, name='category'),
    # 文章分类列表
    path('tag-<int:tag_id>/', views.tag, name='tag'),
    # 文章标签列表
    path('show-<int:article_id>/', views.show, name='show'),
    # 文章内容页
    path('timeAxis/', views.timeAxis, name='timeAxis'),
    # 时间轴
    path('messageBoard/', views.messageBoard, name='messageBoard'),
    # 留言板
    path('about/', views.about, name='about'),
    # 关于
    path('blogroll/', views.blogroll, name='blogroll'),
    # 友情链接
<<<<<<< HEAD
    path('categoryPage', views.categoryPage, name='categoryPage'),
=======

    path('categoryPage/', views.categoryPage, name='categoryPage')
>>>>>>> cf50a96be9e61e0db8f7d6fa591c49e0546d170e
    # ajax文章分类分页
]
