from django.contrib.auth.models import User
from blog.models import Article
from django.db import models


# Create your models here.
# 用户详细信息表，信息可以为空


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    # 与自带用户表一对一
    phone = models.CharField(verbose_name='手机', max_length=20, default="保密")
    sex_choice = [('1', '男'), ('2', '女')]
    sex = models.CharField(verbose_name='性别', max_length=1, choices=sex_choice, default=1)
    web = models.CharField(verbose_name='个人网站', max_length=50, default="保密")
    aboutme = models.TextField(verbose_name='个性签名', max_length=200, default="保密")
    photo = models.ImageField(upload_to='photo/', verbose_name='头像', default='photo/default.png')

    class Meta:
        verbose_name = '用户详细信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "user:{}".format(self.user.username)


# 用户浏览文章记录表
class ArticleViewHistory(models.Model):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='文章名')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='用户名')
    time = models.DateTimeField(auto_now_add=True, verbose_name='浏览时间')
    is_like = models.BooleanField(verbose_name='是否收藏', default=0)

    class Meta:
        ordering = ('-time',)
        verbose_name = '用户浏览文章记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "article:{0},username:{1}".format(self.article, self.user.username)
