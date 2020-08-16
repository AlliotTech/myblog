from django.shortcuts import render

# Create your views here.


# 登录注册
def loginRegister(request):
    return render(request, 'account/loginRegister.html', locals())


# 忘记密码
def forgetPassword(request):
    return render(request, 'account/forgetPassword.html', locals())
