from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
# Create your views here.


# 登录注册
def loginRegister(request):
    if request.method == "POST":
        reqtype = request.POST.get('type')
        if reqtype == "登录":
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            try:
                user = auth.authenticate(username=username, password=password)
                if user:
                    auth.login(request, user)  # session写操作
                    request.session['is_login'] = True
                    return HttpResponseRedirect('/')
                else:
                    message = "密码不正确！"
                    return render(request, 'account/loginRegister.html', locals())
            except:
                message = "用户名不存在！"
                return render(request, 'account/loginRegister.html', locals())
                # print(message)

        if reqtype == "注册":
            print("是注册")
        return render(request, 'account/loginRegister.html', locals())
    else:
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

