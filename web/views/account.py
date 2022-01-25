'''
用户相关功能
'''
from django.core.validators import RegexValidator
from django.shortcuts import render


from django import forms
from web import models

class RegisterModelForm(forms.ModelForm):
    mobile_phone = forms.CharField(label = '手机号',
                                   validators=[RegexValidator(r'^^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$','手机号错误'),])
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'placeholder':'请输入密码'}))
    confirm_password = forms.CharField(label='重复密码',
                                       widget=forms.PasswordInput(attrs={'placeholder':'请重复输入密码'}))
    code = forms.CharField(label='验证码',
                           widget=forms.TextInput(attrs={'placheholder':'请输入密码'}))
    class Meta:
        model = models.UserInfo
        #控制页面顺序

        fields = ['username','email','password','confirm_password','mobile_phone','code']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            # field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)
            field.widget.attrs['placeholder'] = '请输入'+f'{field.label}'

def register(request):
    return render(request,'register.html')