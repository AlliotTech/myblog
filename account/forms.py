from django import forms


class LoginForm(forms.Form):
    # 输入用户名密码登录表单
    username = forms.CharField(max_length=128,
                               error_messages={'required': '用户名不能为空'},
                               widget=forms.TextInput(attrs={'class': 'form-style',
                                                             'placeholder': '用户名',
                                                             'oninvalid': 'setCustomValidity("请输入用户名");',
                                                             'oninput': 'setCustomValidity("");'}))
    password = forms.CharField(max_length=256,
                               error_messages={'required': '密码不能为空'},
                               widget=forms.PasswordInput(attrs={'class': 'form-style',
                                                                 'placeholder': '密码',
                                                                 'oninvalid': 'setCustomValidity("请输入密码");',
                                                                 'oninput': 'setCustomValidity("");'}))
