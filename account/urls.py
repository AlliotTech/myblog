from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('loginRegister/', views.loginRegister, name='loginRegister'),
    # 登录注册
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
