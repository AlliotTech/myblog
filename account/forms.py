from django import forms


class LoginForm(forms.Form):
    # 输入用户名密码登录表单
    username = forms.CharField(max_length=128,
                               error_messages={'required': '用户名不能为空'},
                               widget=forms.TextInput(attrs={'class': 'form-style'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-style'}))

