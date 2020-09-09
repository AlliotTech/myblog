from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "account"

urlpatterns = [
    path('loginRegister/', views.loginRegister, name='loginRegister'),
    # 登录注册页
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    # 注销
    path('forgetPassword/', views.forgetPassword, name='forgetPassword'),
    # 忘记密码
    path('personalCenter/', views.personalCenter, name='personalCenter'),
    # 个人中心
    path('changeInformation/', views.changeInformation, name='changeInformation'),
    # 修改信息
    path('changePassword/', views.changePassword, name='changePassword'),
    # 修改密码
    path('historyBrowse/', views.historyBrowse, name='historyBrowse'),
    # 浏览记录
    path('historyComment/', views.historyComment, name='historyComment'),
    # 评论记录
    path('historyCollection/', views.historyCollection, name='historyCollection'),
    # 收藏记录
    path('historyLeave/', views.historyLeave, name='historyLeave'),
    # 留言记录


    path('registerCheck', views.registerCheck, name='registerCheck'),
    # ajax用户注册信息验证
    path('photoUpload/', views.photoUpload, name='photoUpload'),
    # ajax头像上传
    path('registerCode/', views.registerCode, name='registerCode'),
    # ajax获取注册邮件验证码
    path('forgetCode/', views.forgetCode, name='forgetCode'),
    # ajax获取注册邮件验证码
]
