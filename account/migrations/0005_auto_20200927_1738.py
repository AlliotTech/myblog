# Generated by Django 3.1.1 on 2020-09-27 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200927_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleviewhistory',
            name='time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='浏览时间'),
        ),
    ]