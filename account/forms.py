from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.models import User

from account.models import UserInfo


class LoginForm(forms.Form):
    # 输入用户名密码登录表单
    user = forms.CharField(
        max_length=16,
        error_messages={'required': '用户名不能为空'},
        widget=forms.TextInput(attrs={'class': 'form-style',
                                      'placeholder': '用户名',
                                      'oninvalid': 'setCustomValidity("请输入用户名");',
                                      'oninput': 'setCustomValidity("");'}))
    password = forms.CharField(
        max_length=16,
        error_messages={'required': '密码不能为空'},
        widget=forms.PasswordInput(attrs={'class': 'form-style',
                                          'placeholder': '密码',
                                          'oninvalid': 'setCustomValidity("请输入密码");',
                                          'oninput': 'setCustomValidity("");'}))

    captcha = CaptchaField(
        required=True,
        error_messages={'required': '验证码不能为空'},
    )


class RegisterForm(forms.Form):
    # 用户注册表单
    username = forms.CharField(max_length=10,
                               error_messages={'required': '用户名不能为空'},
                               widget=forms.TextInput(attrs={'class': 'form-style',
                                                             'placeholder': '用户名',
                                                             'oninvalid': 'setCustomValidity("请输入用户名");',
                                                             'oninput': 'setCustomValidity("");'}))
    email = forms.CharField(max_length=50,
                            error_messages={'required': '邮箱号不能为空'},
                            widget=forms.EmailInput(attrs={'class': 'form-style',
                                                           'placeholder': '邮箱号',
                                                           'oninvalid': 'setCustomValidity("请输入邮箱号");',
                                                           'oninput': 'setCustomValidity("");'}))
    password1 = forms.CharField(max_length=16,
                                error_messages={'required': '密码不能为空'},
                                widget=forms.PasswordInput(attrs={'class': 'form-style',
                                                                  'placeholder': '密码',
                                                                  'oninvalid': 'setCustomValidity("请输入密码");',
                                                                  'oninput': 'setCustomValidity("");'}))
    password2 = forms.CharField(max_length=16,
                                error_messages={'required': '密码不能为空'},
                                widget=forms.PasswordInput(attrs={'class': 'form-style',
                                                                  'placeholder': '确认密码',
                                                                  'oninvalid': 'setCustomValidity("请输入密码");',
                                                                  'oninput': 'setCustomValidity("");'}))

    class Meta:
        model = User
        fields = ("username", "email")


class UserInfoForm(forms.ModelForm):
    # 用户修改信息表单
    class Meta:
        model = UserInfo
        fields = ("phone", "sex", "web", "aboutme", "photo",)


class UserForm(forms.ModelForm):
    # 用户信息表单
    class Meta:
        model = User
        fields = ("email",)
