from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt
from account.views import imgSave
from blog.models import Category, Tag, Article
from management.models import About, WebsiteConfig, ImagesConfig, Info, Carousel


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
    return render(request, 'layui-mini/management/articleList.html', locals())


# 文章分类
@xframe_options_exempt
@login_required()
def articleCategory(request):
    return render(request, 'layui-mini/management/articleCategory.html', locals())


# 文章标签
@xframe_options_exempt
@login_required()
def articleTag(request):
    return render(request, 'layui-mini/management/articleTag.html', locals())


# 文章评论
@xframe_options_exempt
@login_required()
def articleComment(request):
    return render(request, 'layui-mini/management/articleComment.html', locals())


# 网站关于
@xframe_options_exempt
@login_required()
def websiteAbout(request):
    if request.method == "POST":
        try:
            about = About.objects.get(id=1)
            about.body = request.POST.get("content")
            about.save()
            result = {
                "code": "1",
                "msg": "修改成功!",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "修改失败!",
            }
        return JsonResponse(result)
    else:
        about = About.objects.get(id=1)
        body = about.body
        time = about.time
        return render(request, 'layui-mini/management/websiteAbout.html', locals())


# 网站配置
@xframe_options_exempt
@login_required()
def websiteConfig(request):
    if request.method == "POST":
        website = WebsiteConfig.objects.get(id=1)
        website.name = request.POST.get('sitename')
        website.domain = request.POST.get('domain')
        website.index_title = request.POST.get('title')
        website.keywords = request.POST.get('keywords')
        website.descript = request.POST.get('descript')
        website.copyright = request.POST.get('copyright')
        images = ImagesConfig.objects.get(id=1)
        images.foreground = request.POST.get('foreground')[6:]
        images.background = request.POST.get('background')[6:]
        images.icon = request.POST.get('icon')[6:]
        images.photo = request.POST.get('photo')[6:]
        images.cover = request.POST.get('cover')[6:]
        images.pay = request.POST.get('pay')[6:]
        try:
            website.save()
            images.save()
            result = {
                "code": "1",
                "msg": "修改成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "修改成功！",
            }
        return JsonResponse(result)
    else:
        website = WebsiteConfig.objects.get(id=1)
        images = ImagesConfig.objects.get(id=1)
        return render(request, 'layui-mini/management/websiteConfig.html', locals())


# 博主信息
@xframe_options_exempt
@login_required()
def BloggerInfo(request):
    if request.method == 'POST':
        info = Info.objects.get(id=1)
        info.position = request.POST.get('position')
        info.company = request.POST.get('company')
        info.location = request.POST.get('location')
        info.email = request.POST.get('email')
        info.csdn = request.POST.get('csdn')
        info.github = request.POST.get('github')
        info.qq = request.POST.get('qq')[6:]
        info.weixin = request.POST.get('weixin')[6:]
        try:
            info.save()
            result = {
                "code": "1",
                "msg": "修改成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "修改失败！",
            }
        return JsonResponse(result)
    else:
        info = Info.objects.get(id=1)
        return render(request, 'layui-mini/management/bloggerInfo.html', locals())


# 留言管理
@xframe_options_exempt
@login_required()
def websiteLeaveMessage(request):
    return render(request, 'management/websiteLeaveMessage.html', locals())


# 轮播图管理
@xframe_options_exempt
@login_required()
def websiteCarousel(request):
    return render(request, 'layui-mini/management/websiteCarousel.html', locals())


# 新增轮播图
@xframe_options_exempt
@login_required()
def carouselAdd(request):
    if request.method == 'POST':
        info = request.POST.get('info')
        url = request.POST.get('url')
        img = request.POST.get('img')[6:]
        is_show = request.POST.get('is_show')
        print(info, url, img, is_show)
        print(request.POST.get('img')[6:])
        carousel = Carousel()
        carousel.info = request.POST.get('info')
        carousel.url = request.POST.get('url')
        carousel.img = request.POST.get('img')[6:]
        carousel.is_show = request.POST.get('is_show')
        try:
            carousel.save()
            result = {
                "code": "1",
                "msg": "添加成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "添加失败！",
            }
        return JsonResponse(result)
    else:
        return render(request, 'layui-mini/management/carouselAdd.html', locals())


# 友情链接管理
@xframe_options_exempt
@login_required()
def websiteLink(request):
    return render(request, 'layui-mini/management/websiteLink.html', locals())


# 用户管理
@xframe_options_exempt
@login_required()
def managementUser(request):
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
            if article_type == 'release':
                article.is_release = 1
            elif article_type == 'save':
                article.is_release = 0
            article.save()
            article.tags.add(*list(Tag.objects.filter(id__in=tags.split(','))))
            result = {
                "code": "1",
                "msg": "提交成功！",
            }
        except Exception as e:
            print(e)
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
    article_arr = request.GET.get("delidArr")
    if article_id:
        Article.objects.get(id=article_id).delete()
        result = {"code": 1, "msg": "删除成功!"}
    elif article_arr:
        article_list = article_arr.split(',')
        for i in article_list:
            Article.objects.get(id=i).delete()
        result = {"code": 1, "msg": "删除成功!"}
    else:
        result = {"code": 0, "msg": "删除失败!"}
    return JsonResponse(result)


# ajax文章修改
@xframe_options_exempt
@login_required()
def articleEdit(request, article_id):
    if request.method == "POST":
        article_id = request.POST.get("id")
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
            article = Article.objects.get(id=article_id)
            article.title = title
            article.excerpt = excerpt
            article.img = img
            article.body = content
            article.author_id = request.user.id
            article.category_id = category_id
            article.is_recommend = recommended
            if article_type == 'release':
                article.is_release = 1
            elif article_type == 'save':
                article.is_release = 0
            article.save()
            article.tags.clear()
            article.tags.add(*list(Tag.objects.filter(id__in=tags.split(','))))
            result = {
                "code": "1",
                "msg": "提交成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "提交失败！",
            }
        return JsonResponse(result)
    else:
        article = Article.objects.get(id=article_id)
        category_all = Category.objects.all()
        tag_all = Tag.objects.all()
        tags = list(article.tags.values_list('id', flat=True))
        return render(request, 'layui-mini/management/articleEdit.html', locals())


# ajax删除文章分类
def categoryDel(request):
    category_id = request.GET.get("del_id")
    category_arr = request.GET.get("delidArr")
    if category_id:
        Category.objects.get(id=category_id).delete()
        result = {"code": 1, "msg": "删除成功!"}
    elif category_arr:
        category_list = category_arr.split(',')
        for i in category_list:
            Category.objects.get(id=i).delete()
        result = {"code": 1, "msg": "删除成功!"}
    else:
        result = {"code": 0, "msg": "删除失败!"}
    return JsonResponse(result)


# ajax修改文章分类
def categoryEdit(request):
    if request.method == "POST":
        category_id = request.POST.get("category_id")
        name = request.POST.get("name")
        try:
            category = Category.objects.get(id=category_id)
            category.name = name
            category.save()
            result = {
                "code": "1",
                "msg": "修改成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "修改失败！",
            }
        return JsonResponse(result)


# ajax新增文章分类
def categoryAdd(request):
    if request.method == "POST":
        name = request.POST.get("name")
        try:
            category = Category()
            category.name = name
            category.save()
            result = {
                "code": "1",
                "msg": "添加成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "添加失败！",
            }
        return JsonResponse(result)


# ajax添加文章标签
def tagAdd(request):
    if request.method == "POST":
        name = request.POST.get("name")
        try:
            tag = Tag()
            tag.name = name
            tag.save()
            result = {
                "code": "1",
                "msg": "添加成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "添加失败！",
            }
        return JsonResponse(result)


# ajax 修改文章标签
def tagEdit(request):
    if request.method == "POST":
        tag_id = request.POST.get("tag_id")
        name = request.POST.get("name")
        try:
            tag = Tag.objects.get(id=tag_id)
            tag.name = name
            tag.save()
            result = {
                "code": "1",
                "msg": "修改成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "修改失败！",
            }
        return JsonResponse(result)


# ajax删除标签
def tagDel(request):
    tag_id = request.GET.get("del_id")
    tag_arr = request.GET.get("delidArr")
    if tag_id:
        Tag.objects.get(id=tag_id).delete()
        result = {"code": 1, "msg": "删除成功!"}
    elif tag_arr:
        tag_list = tag_arr.split(',')
        for i in tag_list:
            Tag.objects.get(id=i).delete()
        result = {"code": 1, "msg": "删除成功!"}
    else:
        result = {"code": 0, "msg": "删除失败!"}
    return JsonResponse(result)


# ajax删除轮播图
def carouselDel(request):
    tag_id = request.GET.get("del_id")
    tag_arr = request.GET.get("delidArr")
    if tag_id:
        Carousel.objects.get(id=tag_id).delete()
        result = {"code": 1, "msg": "删除成功!"}
    elif tag_arr:
        tag_list = tag_arr.split(',')
        for i in tag_list:
            Carousel.objects.get(id=i).delete()
        result = {"code": 1, "msg": "删除成功!"}
    else:
        result = {"code": 0, "msg": "删除失败!"}
    return JsonResponse(result)


# ajax编辑轮播图
@xframe_options_exempt
@login_required()
def carouselEdit(request, carousel_id):
    if request.method == "POST":
        try:
            result = {
                "code": "1",
                "msg": "提交成功！",
            }
        except Exception as e:
            print(e)
            result = {
                "code": "0",
                "msg": "提交失败！",
            }
        return JsonResponse(result)
    else:
        carousel = Carousel.objects.get(id=carousel_id)
        return render(request, 'layui-mini/management/carouselEdit.html', locals())
