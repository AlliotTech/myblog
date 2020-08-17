from django.shortcuts import render

# Create your views here.


# 后台管理dashboard
def dashboard(request):
    return render(request, 'management/dashboard.html', locals())


# 新增文章
def articleAdd(request):
    return render(request, 'management/articleAdd.html', locals())


# 文章列表
def articleList(request):
    articleList = []
    for i in range(1, 11):
        articleList.append(i)
    return render(request, 'management/articleList.html', locals())


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