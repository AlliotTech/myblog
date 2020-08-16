from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('classify/', views.classify, name='classify'),
    # 文章分类列表
    path('show/', views.show, name='show'),
    # 文章内容页
    path('timeAxis/', views.timeAxis, name='timeAxis'),
    # 时间轴
    path('messageBoard/', views.messageBoard, name='messageBoard'),
    # 留言板
    path('about/', views.about, name='about'),
    # 关于
    path('blogroll/', views.blogroll, name='blogroll'),
    # 友情链接
]
