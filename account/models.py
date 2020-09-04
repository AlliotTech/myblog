from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class UserInfo(models.Model):
    # 用户详细信息表，信息可以为空
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    # 与自带用户表一对一
    phone = models.CharField(verbose_name='手机', max_length=20, null=True, blank=True)
    sex_choice = (
        ('1', '男'),
        ('2', '女')
    )
    sex = models.CharField(verbose_name='性别', max_length=1, choices=sex_choice, default=1)
    web = models.URLField(verbose_name='个人网站', null=True, blank=True)
    aboutme = models.TextField(verbose_name='个性签名', null=True, blank=True)
    photo = models.ImageField(upload_to='photo/', verbose_name='头像', null=True, blank=True)

    class Meta:
        verbose_name = '用户详细信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "user:{}".format(self.user.username)
