# Generated by Django 3.1.1 on 2020-10-10 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_article_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_release',
            field=models.BooleanField(default=True, verbose_name='是否发布'),
        ),
    ]
