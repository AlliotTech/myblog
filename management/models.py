from django.db import models

# Create your models here.


from mdeditor.fields import MDTextField


# 轮播图
class Carousel(models.Model):
    img = models.ImageField('轮播图', upload_to='carousel/')
    url = models.URLField('图片链接', max_length=100)
    info = models.CharField('图片标题', max_length=50, default='')

    def __str__(self):
        return self.info

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = '轮播图'


# 友情链接
class Link(models.Model):
    logo = models.ImageField('网站图标', upload_to='logo/')
    name = models.CharField('链接名称', max_length=20)
    url = models.URLField('网址', max_length=100)
    describe = models.CharField('图片标题', max_length=50, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = '友情链接'


# 关于
class About(models.Model):
    body = MDTextField()
    time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '关于'
        verbose_name_plural = '关于'
