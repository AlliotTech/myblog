# Generated by Django 3.1 on 2020-09-01 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200821_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='recommend',
            field=models.BooleanField(default=False, verbose_name='是否推荐显示'),
        ),
    ]