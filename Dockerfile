FROM python:latest
RUN pip install django -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install django-simple-captcha -i https://pypi.tuna.tsinghua.edu.cn/simple