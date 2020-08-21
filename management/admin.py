from django.contrib import admin
from management.models import Carousel, Link
# Register your models here.


# 轮播图
@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('id', 'info', 'img', 'url')


# 友情链接
@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'logo', 'name', 'url', 'describe')

