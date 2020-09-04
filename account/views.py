from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from account.forms import *
from account.models import UserInfo
from django.utils import timezone

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
    userinfo = UserInfo.objects.get(user_id=request.user.id)
    user = User.objects.get(username=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() and userinfo_form.is_valid():
            user_data = user_form.cleaned_data
            userinfo_data = userinfo_form.cleaned_data
            request.user.email = user_data['email']
            userinfo.sex = userinfo_data['sex']
            # userinfo.photo = userinfo_data['photo']
            userinfo.phone = userinfo_data['phone']
            userinfo.web = userinfo_data['web']
            userinfo.aboutme = userinfo_data['aboutme']
            request.user.save()
            userinfo.save()
        return HttpResponseRedirect('/account/personalCenter/')
    else:
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


# 收藏记录
def historyCollection(request):
    collectionList = []
    for i in range(1, 11):
        collectionList.append(i)
    return render(request, 'account/historyCollection.html', locals())


# 留言记录
def historyLeave(request):
    scoreList = []
    for i in range(1, 11):
        scoreList.append(i)
    return render(request, 'account/historyLeave.html', locals())


# 头像上传
def photoUpload(request):
    if request.method == "POST":
        dir = 'photo/'
        file = request.FILES.get('file')
        filename = "%s.%s" % (timezone.now().strftime('%Y_%m_%d_%H_%M_%S_%f'), file.name.split('.')[-1])
        filepath = 'media/' + dir +filename
        # 图片资源写入服务器
        code = upload(file, filepath)
        if (code == 1):
            # 图片路径写入数据库
            url = dir+filename
            print(url)
            userinfo = UserInfo.objects.get(user_id=request.user.id)
            print(userinfo.photo)
            userinfo.photo = url
            userinfo.save()
            data = {
                "msg": "上传成功",
                "src": filepath,
                "code": "1",
            }
            return JsonResponse(data)
        else:
            data = {
                "msg": "上传失败",
                "code": "0",
            }
        return JsonResponse(data)


# 图片保存
def upload(file, filepath):
    try:
        with open(filepath, 'wb+') as f:
            for chrunk in file.chunks():
                f.write(chrunk)
        f.close()
        return 1
    except:
        return 0



