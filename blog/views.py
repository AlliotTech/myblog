from typing import List

from django.shortcuts import render

# Create your views here.


# 首页
def index(request):
    newArticle = []
    # 最新文章列表
    for i in range(1, 11):
        newArticle.append(i)
    topArticle = []
    # 热门文章列表
    for i in range(1, 10):
        topArticle.append(i)
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
def show(request):
    topArticle = []
    # 热门文章列表
    for i in range(1, 10):
        topArticle.append(i)
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
