from typing import List

from django.shortcuts import render
from django.http import HttpResponse
from blog.models import *
from PIL import Image
# 图片压缩处理
# Create your views here.


# 全局调用函数,
def global_variable(request):
    tags = Tag.objects.all()
    hotArticle = Article.objects.all().order_by('-views')[:9]
    categorys = Category.objects.all()
    return locals()


# 图片压缩处理
def compressImage(request):

    picture_list = Article.objects.all()

    for cp in picture_list:
        image = Image.open(cp.img)  # 通过cp.picture 获得图像
        width = image.width
        height = image.height
        rate = 1.0
        # 压缩率

        # 根据图像大小设置压缩率
        if width >= 2000 or height >= 2000:
            rate = 0.3
        elif width >= 1000 or height >= 1000:
            rate = 0.5
        elif width >= 500 or height >= 500:
            rate = 0.9

        width = int(width * rate)
        # 新的宽
        height = int(height * rate)
        # 新的高

        image.thumbnail((width, height), Image.ANTIALIAS)
        # 生成缩略图
        image.save('media/' + str(cp.img), 'JPEG')
        # 保存到原路径
        cp.save()
    return HttpResponse('compress ok')


# 首页
def index(request):
    articles = Article.objects.all().order_by('-created_time')[:10]
    return render(request, 'blog/index.html', locals())


# 文章分类列表
def classify(request):
    classArticle = []
    # 最新文章列表
    for i in range(1, 11):
        classArticle.append(i)
    topArticle = []
    # 热门文章列表
    for i in range(1, 10):
        topArticle.append(i)
    return render(request, 'blog/list.html', locals())


# 文章内容页
def show(request, article_id):
    topArticle = []
    # 热门文章列表
    for i in range(1, 10):
        topArticle.append(i)
    article = Article.objects.get(id=article_id)
    return render(request, 'blog/show.html', locals())


# 时间轴
def timeAxis(request):
    topArticle = []
    # 热门文章列表
    for i in range(1, 10):
        topArticle.append(i)
    return render(request, 'blog/timeAxis.html', locals())


# 留言板
def messageBoard(request):
    topArticle = []
    # 热门文章列表
    for i in range(1, 10):
        topArticle.append(i)
    return render(request, 'blog/messageBoard.html', locals())


# 关于
def about(request):
    topArticle = []
    # 热门文章列表
    for i in range(1, 10):
        topArticle.append(i)
    return render(request, 'blog/about.html', locals())


# 友情链接
def blogroll(request):
    return render(request, 'blog/blogroll.html', locals())
