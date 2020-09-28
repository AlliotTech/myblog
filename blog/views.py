from typing import List

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader

from blog.forms import searchForm
from blog.models import *
from account.models import UserInfo, ArticleViewHistory
from PIL import Image


# Create your views here.


# 全局调用函数,
def global_variable(request):
    # 登录用户信息头像
    if request.user.id is not None:
        userinfo = UserInfo.objects.get(user_id=request.user.id)
    # 所有分类
    categorys = Category.objects.all()
    # 搜索表单
    search_form = searchForm()
    return locals()


# 侧边栏内容
def aside():
    # 所有标签
    tags = Tag.objects.all()
    # 推荐阅读
    recommend = Article.objects.all().filter(recommend=True).order_by('-created_time')[:6]
    # 阅读排行
    viewTop = Article.objects.all().order_by('-view')[:9]
    # 点赞排行
    likeTop = Article.objects.all().order_by('-like')[:9]
    # 收藏排行
    collectionTop = Article.objects.all().order_by('-collection')[:9]
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
    aside_dict = aside()
    count = Article.objects.all().count()
    page_count = (count // 5) + 1
    return render(request, 'blog/index.html', locals())


# 首页流加载
def indexPage(request):
    page_index = request.GET.get('page')
    # 前台传来的一页显示多少条数据
    page_limit = request.GET.get('limit')
    articles_all = Article.objects.all()
    # 处理成LayUi官方文档的格式
    lis = []
    for article in articles_all:
        data = dict()
        data['id'] = article.id
        data['title'] = article.title
        data['excerpt'] = article.excerpt
        data['category'] = article.category.name
        data['category_id'] = article.category_id
        tags = []
        for tag in article.tags.all():
            tags.append(tag.name)
        data['tags'] = tags
        data['img'] = article.img.name
        data['view'] = article.view
        data['like'] = article.like
        data['collection'] = article.collection
        # 格式化时间的格式
        data_joined = article.created_time.strftime("%Y-%m-%d %H:%M:%S")
        data['created_time'] = data_joined
        lis.append(data)
    # 分页器进行分配
    try:
        paginator = Paginator(lis, page_limit)
        # 前端传来页数的数据
        data = paginator.page(page_index)
        # 放在一个列表里
        articles_info = [x for x in data]
        result = {"code": 1,
                  "msg": "分页正常",
                  "count": articles_all.count(),
                  "data": articles_info}
    except:
        result = {"code": 0,
                  "msg": "分页调用异常！"
                  }
    return JsonResponse(result)


# 文章分类列表
def category(request, category_id):
    articles_all = Article.objects.filter(category_id=category_id)
    count = articles_all.count()
    category_name = Category.objects.get(id=category_id)
    return render(request, 'blog/categoryList.html',
                  {"count": count, "category_name": category_name, "category_id": category_id, "aside_dict": aside()})


# ajax文章分类分页
def categoryPage(request):
    category_id = request.GET.get('category_id')
    # 前台传来的页数
    page_index = request.GET.get('page')
    # 前台传来的一页显示多少条数据
    page_limit = request.GET.get('limit')
    articles_all = Article.objects.filter(category_id=category_id)
    # 处理成LayUi官方文档的格式
    lis = []
    for article in articles_all:
        data = dict()
        data['id'] = article.id
        data['title'] = article.title
        data['excerpt'] = article.excerpt
        data['category'] = article.category.name
        data['category_id'] = article.category_id
        data['img'] = article.img.name
        data['view'] = article.view
        data['like'] = article.like
        data['collection'] = article.collection
        # 格式化时间的格式
        data_joined = article.created_time.strftime("%Y-%m-%d %H:%M:%S")
        data['created_time'] = data_joined
        lis.append(data)
    # 分页器进行分配
    try:
        paginator = Paginator(lis, page_limit)
        # 前端传来页数的数据
        data = paginator.page(page_index)
        # 放在一个列表里
        articles_info = [x for x in data]
        result = {"code": 1,
                  "msg": "分页正常",
                  "count": articles_all.count(),
                  "data": articles_info}
    except:
        result = {"code": 0,
                  "msg": "分页调用异常！"
                  }
    return JsonResponse(result)


# 文章标签列表
def tag(request, tag_id):
    aside_dict = aside()
    tag_obj = Tag.objects.get(id=tag_id)
    count = tag_obj.article_set.all().count()
    return render(request, 'blog/tagList.html',
                  {"count": count, "tag_name": tag_obj, "tag_id": tag_id})


# 标签列表分页
def tagPage(request):
    tag_id = request.GET.get('tag_id')
    # 前台传来的页数
    page_index = request.GET.get('page')
    # 前台传来的一页显示多少条数据
    page_limit = request.GET.get('limit')
    article_list = []
    tag_obj = Tag.objects.get(id=tag_id)
    article_obj = tag_obj.article_set.all().values()
    for article in article_obj:
        category_name = Category.objects.get(id=article['category_id'])
        article["category"] = category_name
        article_list.append(article)
    lis = []
    for article in article_list:
        data = dict()
        data['id'] = article['id']
        data['title'] = article['title']
        data['excerpt'] = article['excerpt']
        data['category_id'] = article['category_id']
        data['category'] = Category.objects.get(id=article['category_id']).name
        data['img'] = Article.objects.get(id=article['id']).img.name
        data['view'] = article['view']
        data['like'] = article['like']
        data['collection'] = article['collection']
        # 格式化时间的格式
        data_joined = article['created_time'].strftime("%Y-%m-%d %H:%M:%S")
        data['created_time'] = data_joined
        lis.append(data)
    try:
        paginator = Paginator(lis, page_limit)
        # 前端传来页数的数据
        data = paginator.page(page_index)
        # 放在一个列表里
        articles_info = [x for x in data]
        result = {"code": 1,
                  "msg": "分页正常",
                  "count": len(article_list),
                  "data": articles_info}
    except Exception as e:
        print(e)
        result = {"code": 0,
                  "msg": "分页调用异常！"
                  }
    return JsonResponse(result)


# 文章内容页
def show(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    # 阅读量+1
    article.view = article.view + 1
    article.save()
    # 用户已登录
    article_like = 0
    if request.user.id:
        # 添加阅读记录
        history = ArticleViewHistory()
        history.article = article
        history.user = request.user
        history.save()
        # 判断是否已收藏文章
        user_list = ArticleViewHistory.objects.filter(article_id=article_id)
        for i in user_list:
            if request.user == i.user and i.is_like == 1:
                article_like = 1
                break
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
    return render(request, 'blog/show.html',
                  {"article": article, "articke_like": article_like, "next_article": next_article,
                   "last_article": last_article, "aside_dict": aside()})


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

    return render(request, 'blog/timeAxis.html', {"date_list": date_list, "aside_dict": aside()})


# 留言板
def messageBoard(request):
    aside_dict = aside()
    return render(request, 'blog/messageBoard.html', locals())


# 关于
def about(request):
    aside_dict = aside()
    return render(request, 'blog/about.html', locals())


# 友情链接
def blogroll(request):
    return render(request, 'blog/blogroll.html', locals())


# 搜索
def search(request):
    key = request.GET.get('key')
    search_form = searchForm(request.GET)
    if search_form.is_valid():
        search_data = search_form.cleaned_data
        articles = Article.objects.filter(
            Q(title__icontains=search_data['key']) | Q(body__icontains=search_data['key']))
        if articles.count() == 0:
            message = '未搜索到匹配内容，请重新输入关键字！'
    else:
        message = '输入内容不合法！'
    return render(request, 'blog/search.html', locals())


# ajax文章点赞
def articleLike(request):
    article_id = request.GET.get('id')
    if article_id:
        article = Article.objects.get(id=article_id)
        article.like = article.like + 1
        article.save()
        result = {"code": 1, "msg": "感谢点赞!"}
    else:
        result = {"code": 0, "msg": "点赞失败!"}
    return JsonResponse(result)


# ajax文章收藏
def articleCollection(request):
    article_id = request.GET.get("article_id")
    user_id = request.GET.get("user_id")
    if article_id and user_id:
        article = Article.objects.get(id=article_id)
        user = User.objects.get(id=user_id)
        # 更新浏览记录表
        history = ArticleViewHistory()
        history.article = article
        history.user = user
        history.is_like = 1
        history.save()
        # 更新文章信息表
        article.collection = article.collection + 1
        article.save()
        result = {"code": 1, "msg": "感谢收藏!"}
    else:
        result = {"code": 0, "msg": "点赞失败!"}
    return JsonResponse(result)


# ajax时间轴文章列表
def timeArticle(request):
    year = request.GET.get("year")
    month = request.GET.get("month")
    if year and month:
        article_list = Article.objects.filter(created_time__year=year).filter(created_time__month=month).order_by(
            '-created_time')
        lis = []
        for article in article_list:
            data = dict()
            data['id'] = article.id
            data['title'] = article.title
            data_joined = article.created_time.strftime("%Y-%m-%d %H:%M")
            data['created_time'] = data_joined
            lis.append(data)
        result = {"code": 1, "data": lis}

    else:
        result = {"code": 0, "msg": "查询失败!"}
    return JsonResponse(result)
