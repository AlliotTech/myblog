from django.shortcuts import render

# Create your views here.


# 登录注册
def loginRegister(request):
    return render(request, 'account/loginRegister.html', locals())


# 忘记密码
def forgetPassword(request):
    return render(request, 'account/forgetPassword.html', locals())


# 个人中心
def personalCenter(request):
    return render(request, 'account/personalCenter.html', locals())


# 修改信息
def changeInformation(request):
    return render(request, 'account/changeInformation.html', locals())


# 修改密码
def changePassword(request):
    return render(request, 'account/changePassword.html', locals())


# 浏览记录
def historyBrowse(request):
    browseList = []
    for i in range(1, 11):
        browseList.append(i)
    return render(request, 'account/historyBrowse.html', locals())


# 评论记录
def historyComment(request):
    commentList = []
    for i in range(1, 11):
        commentList.append(i)
    return render(request, 'account/historyComment.html', locals())


# 点赞记录
def historyLike(request):
    likeList = []
    for i in range(1, 11):
        likeList.append(i)
    return render(request, 'account/historyLike.html', locals())


# 评分记录
def historyScore(request):
    scoreList = []
    for i in range(1, 11):
        scoreList.append(i)
    return render(request, 'account/historyScore.html', locals())

