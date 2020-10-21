from django.contrib import admin
from management.models import Carousel, Link, About, WebsiteConfig, BloggerInfo


# Register your models here.


# 轮播图
@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('id', 'info', 'img', 'url')


# 友情链接
@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'logo', 'name', 'url', 'describe')


# 关于
@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('id', 'time')


# 网站配置
@admin.register(WebsiteConfig)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'index_title', 'keywords', 'descript', 'copyright')


# 博主信息
@admin.register(BloggerInfo)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('position', 'company', 'location', 'email', 'csdn', 'github')
