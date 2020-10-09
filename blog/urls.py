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
    # ajax文章添加收藏
    path('deleteCollection', views.deleteCollection, name='deleteCollection'),
    # ajax文章取消收藏
    path('timeArticle', views.timeArticle, name='timeArticle'),
    # ajax时间轴文章列表
    path('postMessage', views.postMessage, name='postMessage'),
    # ajax发布留言
    path('likeMessage', views.likeMessage, name='likeMessage'),
    # ajax点赞留言
    path('delMessage', views.delMessage, name='delMessage'),
    # ajax删除留言
    path('postComment', views.postComment, name='postComment'),
    # ajax发布留言
    path('likeComment', views.likeComment, name='likeComment'),
    # ajax点赞留言
    path('delComment', views.delComment, name='delComment'),
    # ajax删除留言
]
