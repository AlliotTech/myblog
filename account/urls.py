from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('loginRegister/', views.loginRegister, name='loginRegister'),
    # 登录注册
    path('forgetPassword/', views.forgetPassword, name='forgetPassword'),
    # 忘记密码
]
