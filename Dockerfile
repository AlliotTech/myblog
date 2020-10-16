# 项目dockerfile镜像文件
FROM python:latest
RUN pip install django django-simple-captcha django-mdeditor markdown \
-i https://pypi.tuna.tsinghua.edu.cn/simple