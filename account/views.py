from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from account.forms import *
from account.models import UserInfo
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
                    message = '密码错误'
                    login_form = LoginForm()
                    register_form = RegisterForm()
                    return render(request, "account/loginRegister.html", locals())
            else:
                message = login_form.errors
                login_form = LoginForm()
                register_form = RegisterForm()
                return render(request, "account/loginRegister.html", locals())

        if reqtype == "注册":
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                # 检验通过，创建用户
                username = register_form.cleaned_data['username']
                password1 = register_form.cleaned_data['password1']
                password2 = register_form.cleaned_data['password2']
                email = register_form.cleaned_data['email']
                new_user = User.objects.create()
                new_user.username = username
                new_user.set_password(password1)
                new_user.email = email
                new_user.save()
                message = '您已成功注册，快来登录吧！'
                return HttpResponseRedirect('/account/loginRegister')
            else:
                message = register_form.errors
                login_form = LoginForm()
                register_form = RegisterForm()
                return render(request, "account/loginRegister.html", locals())
        return render(request, 'account/loginRegister.html', locals())
    else:
        login_form = LoginForm()
        register_form = RegisterForm()
        return render(request, 'account/loginRegister.html', locals())


# 忘记密码
def forgetPassword(request):
    return render(request, 'account/forgetPassword.html', locals())



@login_required()
# 判断用户是否登录，django自带的装饰器函数
# 个人中心
def personalCenter(request):
    userinfo = UserInfo.objects.get(user_id=request.user.id)
    user = User.objects.get(username=request.user)
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

