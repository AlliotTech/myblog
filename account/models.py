from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class UserInfo(models.Model):
    # 用户详细信息表，信息可以为空
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
