from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from myblog import settings
from account.forms import *
from account.models import UserInfo
from django.utils import timezone
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.core.mail import send_mail
import datetime
import random


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
                user = authenticate(username=login_data['user'], password=login_data['password'])
                # 验证账号密码是否正确，正确返回user对象，错误返回null
                if user:
                    login(request, user)
                    # 调用django默认的login方法，实现用户登录
                    return HttpResponseRedirect('/')
                else:
                    message = '用户名或密码错误！'
                    login_form = LoginForm()
                    register_form = RegisterForm()
                    return render(request, "account/loginRegister.html", locals())
            else:
                hashkey = CaptchaStore.generate_key()
                image_url = captcha_image_url(hashkey)
                message = login_form.errors
                login_form = LoginForm()
                register_form = RegisterForm()
                return render(request, "account/loginRegister.html", locals())

        if reqtype == "注册":
            print("注册了")
            # 校验邮件验证码
            request_code = request.POST.get('email_code')
            try:
                session_code = request.session['email_code']
            except KeyError:
                data = {
                    "code": 3,
                    "msg": "邮件验证码已过期！"
                }
                return JsonResponse(data)
            if request_code != session_code:
                data = {
                    "code": 2,
                    "msg": "邮件验证码错误！"
                }
                return JsonResponse(data)
            # 校验通过，创建用户
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            new_user = User.objects.create()
            new_user.username = username
            new_user.set_password(password)
            new_user.email = email
            new_user.save()
            # 创建用户信息表记录
            UserInfo.objects.create(user_id=new_user.id)
            # 创建完用户自动登录
            user = authenticate(username=username, password=password)
            # 调用django默认的login方法，实现用户登录
            login(request, user)
            data = {
                "code": 1,
                "msg": "注册成功，自动跳转至首页并登陆！"
            }
            return JsonResponse(data)
    else:
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
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
            print(user_form.is_valid())
            print(userinfo_form.is_valid())
            user_data = user_form.cleaned_data
            userinfo_data = userinfo_form.cleaned_data
            request.user.email = user_data['email']
            userinfo.sex = userinfo_data['sex']
            userinfo.phone = userinfo_data['phone']
            userinfo.web = userinfo_data['web']
            userinfo.aboutme = userinfo_data['aboutme']
            request.user.save()
            userinfo.save()
            return HttpResponseRedirect('/account/personalCenter/')
        else:
            return render(request, 'account/changeInformation.html', locals())
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


# ajax用户注册验证
def registerCheck(request):
    username = request.GET.get('username')
    if username is not None:
        if User.objects.filter(username=username).exists():
            data = {
                "code": 0,
                "msg": "用户名已存在"
            }
        else:
            data = {
                "code": 1,
                "msg": "用户名可以使用"
            }
        return JsonResponse(data)
    email = request.GET.get('email')
    if email is not None:
        if User.objects.filter(email=email).exists():
            data = {
                "code": 0,
                "msg": "邮箱已注册"
            }
        else:
            data = {
                "code": 1,
                "msg": "邮箱可以使用"
            }
        return JsonResponse(data)


# ajax获取邮件验证码
def emailCode(request):
    if request.method == "GET":
        email = request.GET["email"]
        print(email)
        email_code = ""
        for i in range(6):
            email_code = email_code + str(random.randint(0, 9))
        print(email_code)
        request.session['email_code'] = email_code
        # 过期时间 单位s
        request.session.set_expiry(300)
        # request.session['email_code_time'] = email_code_time
        # email_title = '注册账号'
        # email_body = '欢迎注册账号'
        # email = '16609376866@163.com'  # 对方的邮箱
        # send_status = send_mail(email_title, email_body, settings.DEFAULT_FROM_EMAIL, [email])
        # print(send_status)
        data = {
            "code": 1,
            "msg": "验证码已发送"
        }
    return JsonResponse(data)


# ajax头像上传
def photoUpload(request):
    if request.method == "POST":
        dir = 'photo/'
        file = request.FILES.get('file')
        filename = "%s.%s" % (timezone.now().strftime('%Y_%m_%d_%H_%M_%S_%f'), file.name.split('.')[-1])
        filepath = 'media/' + dir + filename
        # 图片资源写入服务器
        code = upload(file, filepath)
        if (code == 1):
            # 图片路径写入数据库
            url = dir + filename
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
