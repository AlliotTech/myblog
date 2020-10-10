from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.
from account.views import imgSave
from blog.models import Category, Tag, Article


@login_required()
# 后台管理模块
def management(request):
    model = "management"
    return render(request, 'layui-mini/base.html', locals())


# 后台管理首页
@xframe_options_exempt
@login_required()
def dashboard(request):
    return render(request, 'layui-mini/management/index.html', locals())


# 文章列表
@xframe_options_exempt
@login_required()
def articleList(request):
    articleList = []
    for i in range(1, 11):
        articleList.append(i)
    return render(request, 'layui-mini/management/articleList.html', locals())


# 文章分类
def articleClass(request):
    classList = []
    for i in range(1, 11):
        classList.append(i)
    return render(request, 'management/articleClass.html', locals())


# 文章标签
def articleTag(request):
    tagList = []
    for i in range(1, 11):
        tagList.append(i)
    return render(request, 'management/articleTag.html', locals())


# 文章评论
def articleComment(request):
    commentList = []
    for i in range(1, 11):
        commentList.append(i)
    return render(request, 'management/articleComment.html', locals())


# 留言管理
def websiteLeaveMessage(request):
    leaveList = []
    for i in range(1, 11):
        leaveList.append(i)
    return render(request, 'management/websiteLeaveMessage.html', locals())


# 轮播图管理
def websiteCarousel(request):
    carouselList = []
    for i in range(1, 6):
        carouselList.append(i)
    return render(request, 'management/websiteCarousel.html', locals())


# 友情链接管理
def websiteLink(request):
    linkList = []
    for i in range(1, 11):
        linkList.append(i)
    return render(request, 'management/websiteLink.html', locals())


# 用户管理
def managementUser(request):
    userList = []
    for i in range(1, 11):
        userList.append(i)
    return render(request, 'management/managementUser.html', locals())


# ajax 文章封面图片上传
def coverUpload(request):
    if request.method == "POST":
        dir = 'cover/'
        file = request.FILES.get('file')
        filename = "%s.%s" % (timezone.now().strftime('%Y_%m_%d_%H_%M_%S_%f'), file.name.split('.')[-1])
        filepath = 'media/' + dir + filename
        # 图片资源写入服务器
        code = imgSave(file, filepath)
        if (code == 1):
            result = {
                "code": "1",
                "msg": "上传成功!",
                "src": filepath,
            }
            return JsonResponse(result)
        else:
            result = {
                "code": "0",
                "msg": "上传失败!",
                "src": None,
            }
        return JsonResponse(result)


# 新增文章
@xframe_options_exempt
@login_required()
def articleAdd(request):
    if request.method == "POST":
        title = request.POST.get("title")
        category_id = request.POST.get("category_id")
        excerpt = request.POST.get("excerpt")
        tags = request.POST.get("tags")
        cover_img = request.POST.get("cover_img")
        img = str(cover_img).split("media/")[1]
        content = request.POST.get("content")
        article_type = request.POST.get("type")
        recommended = request.POST.get("recommended")
        try:
            article = Article()
            article.title = title
            article.excerpt = excerpt
            article.img = img
            article.body = content
            article.author_id = request.user.id
            article.category_id = category_id
            article.is_recommend = recommended
            if article_type == '发布':
                article.is_release = 1
            elif article_type == '保存':
                article.is_release = 0
            article.save()
            article.tags.add(*list(Tag.objects.filter(id__in=tags.split(','))))
            result = {
                "code": "1",
                "msg": "提交成功！",
            }
        except:
            result = {
                "code": "0",
                "msg": "提交失败！",
            }
        return JsonResponse(result)
    else:
        category_all = Category.objects.all()
        tag_all = Tag.objects.all()
        return render(request, 'layui-mini/management/articleAdd.html', locals())


# ajax删除文章
def articleDel(request):
    article_id = request.GET.get("del_id")
    if article_id:
        Article.objects.get(id=article_id).delete()
        result = {"code": 1, "msg": "删除成功!"}
    else:
        result = {"code": 0, "msg": "删除失败!"}
    return JsonResponse(result)


# ajax文章修改
@xframe_options_exempt
@login_required()
def articleEdit(request, article_id):
    if request.method == "POST":
        pass
    else:
        article = Article.objects.get(id=article_id)
        category_all = Category.objects.all()
        tag_all = Tag.objects.all()
        tags = list(article.tags.values_list('id', flat=True))
        return render(request, 'layui-mini/management/articleEdit.html', locals())
