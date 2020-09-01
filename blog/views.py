from typing import List

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from blog.models import *
from account.models import UserInfo
from PIL import Image
# 图片压缩处理
# Create your views here.


# 全局调用函数,
def global_variable(request):
    # 登录用户信息
    if request.user.id is not None:
        userinfo = UserInfo.objects.get(user_id=request.user.id)
        photo = userinfo.photo
    # 所有标签
    tags = Tag.objects.all()
    # 所有分类
    categorys = Category.objects.all()
    # 推荐阅读
    recommend = Article.objects.all().filter(recommend=True).order_by('-created_time')[:6]
    # 阅读排行
    viewTop = Article.objects.all().order_by('-views')[:9]
    # 点赞排行
    likeTop = Article.objects.all().order_by('-likes')[:9]
    # 评分排行
    scoreTop = Article.objects.all().order_by('-score')[:9]
    # 评论排行

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
def category(request, category_id):
    articles = Article.objects.filter(category_id=category_id)
    categoryName = Category.objects.get(id=category_id)
    return render(request, 'blog/list.html', locals())


# 文章标签列表
def tag(request, tag_id):
    articles = []
    tag_obj = Tag.objects.get(id=tag_id)
    tagName = tag_obj
    article_obj = tag_obj.article_set.all().values()
    for article in article_obj:
        category_name = Category.objects.get(id=article['category_id'])
        article["category"] = category_name
        articles.append(article)
    return render(request, 'blog/list.html', locals())


# 文章内容页
def show(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    # 阅读量+1
    article.views = article.views + 1
    article.save()
    # 下一篇，找出id大于当前文章id的文章,升序排序后取第一个，即为下一篇
    next_article = Article.objects.filter(id__gt=article_id).order_by("id")[:1]
    if len(next_article) == 0:
        next_article = 0
    else:
        for next in next_article:
            next_article = next
    # 上一篇，找出id小于当前文章id的文章，降序排序后取第一个，即为上一篇
    last_article = Article.objects.filter(id__lt=article_id).order_by("-id")[:1]
    if len(last_article) == 0:
        last_article = 0
    else:
        for last in last_article:
            last_article = last
    return render(request, 'blog/show.html', locals())


# 时间轴
def timeAxis(request):
    date_list_all = []  # 建立一个列表用来存放所有日期
    date_obj = Article.objects.all().values('created_time')
    for date in date_obj:
        date = date['created_time'].strftime('%Y年%m月')
        date_list_all.append(date)
    date_list_count = []
    # 日期去重
    for i in date_list_all:
        date_list_count.append(date_list_all.count(i))
    date_list_sum = zip(date_list_all, date_list_count)
    date_list = []
    for (i, j) in date_list_sum:
        if (i, j) not in date_list:
            date_list.append((i, j))

    return render(request, 'blog/timeAxis.html', {"date_list":date_list})


# 留言板
def messageBoard(request):
    return render(request, 'blog/messageBoard.html', locals())


# 关于
def about(request):
    return render(request, 'blog/about.html', locals())


# 友情链接
def blogroll(request):
    return render(request, 'blog/blogroll.html', locals())
