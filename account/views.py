from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import auth
from account.forms import LoginForm
# Create your views here.


# 登录注册
def loginRegister(request):
    if request.method == "POST":
        reqtype = request.POST.get('type')
        if reqtype == "登录":
            login_form = LoginForm(request.POST)
            # 创建一个对象，获得post方法提交的数据
            if login_form.is_valid():
                # 验证传入的数据是否合法
                login_data = login_form.cleaned_data
                # 引入字典数据类型，存储用户名和密码
                user = authenticate(username=login_data['username'], password=login_data['password'])
                # 验证账号密码是否正确，正确返回user对象，错误返回null
                if user:
                    login(request, user)
                    # 调用django默认的login方法，实现用户登录
                    return HttpResponseRedirect('/')
                else:
                    message = '用户名或密码错误'
                    return render(request, "account/loginRegister.html", locals())
            else:
                message = '非法数据'
                return render(request, "account/loginRegister.html", locals())

        if reqtype == "注册":
            pass
        return render(request, 'account/loginRegister.html', locals())
    else:
        login_form = LoginForm()
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

