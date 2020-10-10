from django.db import models
from django.contrib.auth.models import User
# 导入Django自带用户模块
# Create your models here.


# 文章分类
from mdeditor.fields import MDTextField


class Category(models.Model):
    name = models.CharField('文章分类', max_length=100)

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 文章标签
class Tag(models.Model):
    name = models.CharField('文章标签', max_length=100)

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 文章内容
class Article(models.Model):
    title = models.CharField('标题', max_length=70)
    excerpt = models.TextField('摘要', max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='分类', blank=True, null=True)
    # 使用外键关联分类表与分类是一对多关系
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    # 使用外键关联标签表与标签是多对多关系
    img = models.ImageField(upload_to='cover/', verbose_name='文章图片', blank=True, null=True, default='cover/default.jpg')
    body = MDTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    """
    文章作者，这里User是从django.contrib.auth.models导入的。
    这里我们通过 ForeignKey 把文章和 User 关联了起来。
    """
    view = models.PositiveIntegerField('阅读量', default=0)
    like = models.PositiveIntegerField('点赞数', default=0)
    collection = models.PositiveIntegerField('收藏数', default=0)
    comment = models.PositiveIntegerField('评论数', default=0)
    created_time = models.DateTimeField('发布时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)
    is_recommend = models.BooleanField('是否推荐显示', default=False)
    is_release = models.BooleanField('是否发布', default=True)

    class Meta:
        verbose_name = '文章内容'
        verbose_name_plural = '文章内容'
        ordering = ("-created_time",)
        # 默认按创建时间倒序排列

    def __str__(self):
        return self.title





