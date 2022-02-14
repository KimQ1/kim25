import random

from django import forms
from kim25 import settings
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from utils import encrypt

from utils.tencent.sms import send_sms_single
from django_redis import get_redis_connection

class RegisterModelForm(forms.ModelForm):
    mobile_phone = forms.CharField(label = '手机号',
                                   validators=[RegexValidator(r'^^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$','手机号错误'),])
    password = forms.CharField(label='密码',
                               min_length=8,
                               max_length=64,
                               error_messages={
                                   'min_length': '密码长度不能小于8位',
                                   'max_length': '密码长度不能大于64位'
                               },
                               widget=forms.PasswordInput(attrs={'placeholder':'请输入密码'}))
    confirm_password = forms.CharField(label='重复密码',
                                       min_length=8,
                                       max_length=64,
                                       error_messages={
                                           'min_length': '密码长度不能小于8位',
                                           'max_length': '密码长度不能大于64位'
                                       },
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
    def clean_username(self):
        username = self.cleaned_data['username']
        exists = models.UserInfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError('用户名已存在')
        return username
    def clean_email(self):
        email = self.cleaned_data['email']
        exists = models.UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('邮箱已存在')
        return email
    def clean_password(self):
        pwd = self.cleaned_data['password']
        return encrypt.md5(pwd)
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm_pwd = encrypt.md5(self.cleaned_data['confirm_password'])
        if pwd != confirm_pwd:
            raise ValidationError('两次密码不一致')
        return confirm_pwd
    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists =  models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError('手机号已经注册')
        return mobile_phone
    def clean_code(self):
        code = self.cleaned_data['code']
        # moblie_phone = self.cleaned_data['mobile_phone']//因为self.cleaned_data没有值，报错
        moblie_phone = self.cleaned_data.get('mobile_phone')
        if not moblie_phone:
            return code
        conn = get_redis_connection()
        redis_code = conn.get(moblie_phone)
        if not redis_code:
            raise ValidationError('验证码失效或未发送，请重新发送')
        redis_str_code = redis_code.decode('utf-8')
        if code.strip() != redis_str_code:
            raise ValidationError('验证码错误，请重新输入')
        return code


class SendSmsForm(forms.Form):
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(
        r'^^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$', '手机号格式错误'), ])

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(request)
        self.request = request
        print(self.request)

    def clean_mobile_phone(self):
        """ 手机号校验的钩子 """
        mobile_phone = self.cleaned_data['mobile_phone']
        # 判断短信模板是否有问题
        tpl = self.request.GET.get('tpl')
        template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
        if not template_id:
            # self.add_error('mobile_phone','短信模板错误')
            raise ValidationError('短信模板错误')
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if tpl == 'login':
            if not exists:
                raise ValidationError('手机号不存在')
        else:
            # 校验数据库中是否已有手机号
            if exists:
                raise ValidationError('手机号已存在')
        code = random.randrange(1000, 9999)
        # 发送短信
        sms = send_sms_single(mobile_phone, template_id, [code, ])
        if sms['result'] != 0:
            raise ValidationError("短信发送失败，{}".format(sms['errmsg']))
        # 验证码 写入redis（django-redis）
        conn = get_redis_connection()
        conn.set(mobile_phone, code, ex=60)
        return mobile_phone
