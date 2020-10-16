from typing import List
import collections
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Max
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth.models import User
from django.utils import timezone
from blog.forms import searchForm
from blog.models import *
from account.models import UserInfo, ArticleViewHistory, LeaveMessage, CommentMessage
from PIL import Image

# Create your views here.


# 全局调用函数,
from management.models import About


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
    recommend = Article.objects.all().filter(is_recommend=True).filter(is_release=True).order_by('-created_time')[:6]
    # 阅读排行
    viewTop = Article.objects.all().filter(is_release=True).order_by('-view')[:9]
    # 点赞排行
    likeTop = Article.objects.all().filter(is_release=True).order_by('-like')[:9]
    # 收藏排行
    collectionTop = Article.objects.all().filter(is_release=True).order_by('-collection')[:9]
    # 评论排行
    commentTop = Article.objects.all().filter(is_release=True).order_by('-comment')[:9]
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
    count = Article.objects.all().filter(is_release=True).count()
    page_count = (count // 5) + 1
    return render(request, 'blog/index.html', locals())


# 首页流加载
def indexPage(request):
    page_index = request.GET.get('page')
    # 前台传来的一页显示多少条数据
    page_limit = request.GET.get('limit')
    articles_all = Article.objects.all().filter(is_release=True)
    # 处理成LayUi官方文档的格式
    lis = []
    for article in articles_all:
        data = model_to_dict(article)
        data['category'] = article.category.name
        data['img'] = article.img.name
        data['created_time'] = article.created_time.strftime("%Y-%m-%d %H:%M:%S")
        data.pop('tags')
        data.pop('body')
        data['category_id'] = article.category_id
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
    except Exception as e:
        print(e)
        result = {"code": 0,
                  "msg": "分页调用异常！"
                  }
    return JsonResponse(result)


# 文章分类列表
def category(request, category_id):
    articles_all = Article.objects.filter(category_id=category_id).filter(is_release=True)
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
    articles_all = Article.objects.filter(category_id=category_id).filter(is_release=True)
    # 处理成LayUi官方文档的格式
    lis = []
    for article in articles_all:
        data = model_to_dict(article)
        data['category'] = article.category.name
        data['img'] = article.img.name
        data['created_time'] = article.created_time.strftime("%Y-%m-%d %H:%M:%S")
        data.pop('tags')
        data.pop('body')
        data['category_id'] = article.category_id
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
    except Exception as e:
        print(e)
        result = {"code": 0,
                  "msg": "分页调用异常！"
                  }
    return JsonResponse(result)


# 文章标签列表
def tag(request, tag_id):
    tag_obj = Tag.objects.get(id=tag_id)
    count = tag_obj.article_set.all().count()
    return render(request, 'blog/tagList.html',
                  {"count": count, "tag_name": tag_obj, "tag_id": tag_id, "aside_dict": aside()})


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
        article['category'] = Category.objects.get(id=article['category_id']).name
        article['img'] = Article.objects.get(id=article['id']).img.name
        article['created_time'] = article['created_time'].strftime("%Y-%m-%d %H:%M:%S")
        article.pop('body')
        lis.append(article)
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


# 查找根评论的所有子回复
def comment_record(article, root_id, record):
    for comment in CommentMessage.objects.filter(root_id=root_id):
        comment_dict = model_to_dict(comment)
        comment_dict['photo'] = CommentMessage.objects.get(id=comment.id).user.userinfo.photo.name
        comment_dict['username'] = CommentMessage.objects.get(id=comment.id).user.username
        comment_dict['time'] = CommentMessage.objects.get(id=comment.id).time.strftime("%Y-%m-%d %H:%M:%S")
        reply_id = CommentMessage.objects.get(id=comment.id).reply_id
        comment_dict['reply_name'] = CommentMessage.objects.get(id=reply_id).user.username
        record.append(comment_dict)
    return record


# 文章内容页
def show(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    # 阅读量+1
    article.view = article.view + 1
    article.save()
    # 用户已登录
    if request.user.id:
        # 添加阅读记录(第一次：添加，已有记录：更新时间)
        history = ArticleViewHistory.objects.filter(article_id=article_id).filter(user_id=request.user)
        if history:
            change_history = history[0]
            change_history.time = timezone.now()
            change_history.save()
        else:
            new_history = ArticleViewHistory()
            new_history.article = article
            new_history.category = article.category
            new_history.user = request.user
            new_history.save()
        # 判断是否已收藏文章
        article_like = 0
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
    # 评论列表
    # 全部评论
    all_comment = []
    for info in CommentMessage.objects.filter(article=article):
        # 根评论
        if info.reply_id is None:
            # 单条记录
            record = []
            info_dict = model_to_dict(info)
            info_dict['username'] = CommentMessage.objects.get(id=info.id).user.username
            info_dict['reply_id'] = 'None'
            info_dict['root_id'] = 'None'
            info_dict['reply_name'] = 'None'
            info_dict['photo'] = CommentMessage.objects.get(id=info.id).user.userinfo.photo.name
            info_dict['time'] = CommentMessage.objects.get(id=info.id).time.strftime("%Y-%m-%d %H:%M:%S")
            record.append(info_dict)
            # 根据根留言查找子回复
            record = comment_record(article, info.id, record)
            all_comment.append(record)
    # 热门留言
    hot_comment = CommentMessage.objects.filter(article=article).filter(level=0).order_by('-like')
    # 我的留言
    user_id = request.user.id
    if user_id:
        my_comment = CommentMessage.objects.filter(article=article).filter(level=0).filter(user_id=user_id)
    else:
        my_comment = None
    # 留言统计
    count = CommentMessage.objects.filter(article=article).count()
    return render(request, 'blog/show.html',
                  {"article": article, "articke_like": article_like, "next_article": next_article,
                   "last_article": last_article, "all_comment": all_comment, "hot_comment": hot_comment,
                   "my_comment": my_comment, "count": count, "aside_dict": aside()})


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


# 查找根留言的所有子回复
def build_record(root_id, record):
    for comment in LeaveMessage.objects.filter(root_id=root_id):
        comment_dict = model_to_dict(comment)
        comment_dict['photo'] = LeaveMessage.objects.get(id=comment.id).user.userinfo.photo.name
        comment_dict['username'] = LeaveMessage.objects.get(id=comment.id).user.username
        comment_dict['time'] = LeaveMessage.objects.get(id=comment.id).time.strftime("%Y-%m-%d %H:%M:%S")
        reply_id = LeaveMessage.objects.get(id=comment.id).reply_id
        comment_dict['reply_name'] = LeaveMessage.objects.get(id=reply_id).user.username
        record.append(comment_dict)
    return record


# 留言板
def messageBoard(request):
    # 全部留言
    all_message = []
    for info in LeaveMessage.objects.all():
        # 根留言
        if info.reply_id is None:
            # 单条记录
            record = []
            info_dict = model_to_dict(info)
            info_dict['username'] = LeaveMessage.objects.get(id=info.id).user.username
            info_dict['reply_id'] = 'None'
            info_dict['root_id'] = 'None'
            info_dict['reply_name'] = 'None'
            info_dict['photo'] = LeaveMessage.objects.get(id=info.id).user.userinfo.photo.name
            info_dict['time'] = LeaveMessage.objects.get(id=info.id).time.strftime("%Y-%m-%d %H:%M:%S")
            record.append(info_dict)
            # 根据根留言查找子回复
            record = build_record(info.id, record)
            all_message.append(record)
    # 热门留言
    hot_message = LeaveMessage.objects.filter(level=0).order_by('-like')
    # 我的留言
    user_id = request.user.id
    if user_id:
        my_message = LeaveMessage.objects.filter(level=0).filter(user_id=user_id)
    else:
        my_message = None
    # 留言统计
    count = LeaveMessage.objects.all().count()
    return render(request, 'blog/messageBoard.html',
                  {"all_message": all_message, "hot_message": hot_message, "my_message": my_message,
                   "count": count, "aside_dict": aside()})


# ajax发布留言
def postMessage(request):
    content = request.GET.get("content")
    username = request.GET.get("username")
    level = request.GET.get("level")
    if content and username:
        reply_id = request.GET.get("reply_id")
        root_id = request.GET.get("root_id")
        message = LeaveMessage()
        message.content = content
        message.user = User.objects.get(username=username)
        message.level = level
        message.reply_id = reply_id
        message.root_id = root_id
        message.save()
        result = {"code": 1, "msg": "留言成功!"}
    else:
        result = {"code": 0, "msg": "留言失败!"}
    return JsonResponse(result)


# ajax点赞留言
def likeMessage(request):
    message_id = request.GET.get("like_id")
    if message_id:
        message = LeaveMessage.objects.get(id=message_id)
        message.like = message.like + 1
        message.save()
        result = {"code": 1, "msg": "点赞成功!"}
    else:
        result = {"code": 0, "msg": "点赞失败!"}
    return JsonResponse(result)


# ajax删除留言
def delMessage(request):
    message_id = request.GET.get("del_id")
    if message_id:
        message = LeaveMessage.objects.get(id=message_id)
        reply = LeaveMessage.objects.filter(reply_id=message_id)
        # 根留言且没有回复，可以删除
        if message.level == 0 and len(reply) == 0:
            LeaveMessage.objects.get(id=message_id).delete()
        else:
            message.content = "该内容已被用户删除"
            message.save()
        result = {"code": 1, "msg": "删除成功!"}
    else:
        result = {"code": 0, "msg": "删除失败!"}
    return JsonResponse(result)


# 关于
def about(request):
    aside_dict = aside()
    about_content = About.objects.get(id=1)
    return render(request, 'blog/about.html', locals())


# 友情链接
def blogroll(request):
    return render(request, 'blog/blogRoll.html', locals())


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
        # 更新浏览记录表
        history = ArticleViewHistory.objects.filter(article_id=article_id).filter(user_id=request.user)
        change_history = history[0]
        change_history.time = timezone.now()
        change_history.is_like = 1
        change_history.save()
        # 更新文章信息表
        article = Article.objects.get(id=article_id)
        article.collection = article.collection + 1
        article.save()
        result = {"code": 1, "msg": "感谢收藏!"}
    else:
        result = {"code": 0, "msg": "点赞失败!"}
    return JsonResponse(result)


# ajax取消收藏
def deleteCollection(request):
    article_id = request.GET.get("article_id")
    user_id = request.GET.get("user_id")
    delid_arr = request.GET.get("delidArr")
    print(article_id, user_id, delid_arr)
    if article_id:
        # 更新浏览记录表
        history = ArticleViewHistory.objects.filter(article_id=article_id).filter(user_id=request.user)
        change_history = history[0]
        change_history.time = timezone.now()
        change_history.is_like = 0
        change_history.save()
        result = {"code": 1, "msg": "已取消收藏!"}
    elif delid_arr:
        article_list = delid_arr.split(',')
        for i in article_list:
            change_history = ArticleViewHistory.objects.get(id=i)
            change_history.time = timezone.now()
            change_history.is_like = 0
            change_history.save()
        result = {"code": 1, "msg": "已取消收藏!"}
    else:
        result = {"code": 0, "msg": "操作失败!"}
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


# ajax发表评论
def postComment(request):
    article_id = request.GET.get("article_id")
    content = request.GET.get("content")
    username = request.GET.get("username")
    level = request.GET.get("level")
    if content and username:
        reply_id = request.GET.get("reply_id")
        root_id = request.GET.get("root_id")
        message = CommentMessage()
        message.article = Article.objects.get(id=article_id)
        message.content = content
        message.user = User.objects.get(username=username)
        message.level = level
        message.reply_id = reply_id
        message.root_id = root_id
        message.save()
        # 更新评论数
        article = Article.objects.get(id=article_id)
        article.comment = CommentMessage.objects.filter(article=article).count()
        article.save()
        result = {"code": 1, "msg": "评论成功!"}
    else:
        result = {"code": 0, "msg": "评论失败!"}
    return JsonResponse(result)


# ajax点赞评论
def likeComment(request):
    message_id = request.GET.get("like_id")
    if message_id:
        message = CommentMessage.objects.get(id=message_id)
        message.like = message.like + 1
        message.save()
        result = {"code": 1, "msg": "点赞成功!"}
    else:
        result = {"code": 0, "msg": "点赞失败!"}
    return JsonResponse(result)


# ajax删除评论
def delComment(request):
    message_id = request.GET.get("del_id")
    if message_id:
        message = CommentMessage.objects.get(id=message_id)
        reply = CommentMessage.objects.filter(reply_id=message_id)
        # 根留言且没有回复，可以删除
        if message.level == 0 and len(reply) == 0:
            CommentMessage.objects.get(id=message_id).delete()
        else:
            message.content = "该内容已被用户删除"
            message.save()
        result = {"code": 1, "msg": "删除成功!"}
    else:
        result = {"code": 0, "msg": "删除失败!"}
    return JsonResponse(result)
