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
    path('search', views.search, name='search'),
    # 搜索
    path('categoryPage', views.categoryPage, name='categoryPage'),
    # ajax文章分类分页
    path('tagPage', views.tagPage, name='tagPage'),
    # ajax标签分类分页
    path('indexPage', views.indexPage, name='indexPage'),
    # ajax首页流加载
    path('articleLike', views.articleLike, name='articleLike'),
    # ajax文章点赞
    path('articleCollection', views.articleCollection, name='articleCollection'),
    # ajax文章收藏
]
