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
    path('historyLike/', views.historyLike, name='historyLike'),
    # 点赞记录
    path('historyScore/', views.historyScore, name='historyScore'),
    # 评分记录
]
