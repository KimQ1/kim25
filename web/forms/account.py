import random

from django import forms
from kim25 import settings
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from utils.tencent.sms import send_sms_single
from django_redis import get_redis_connection

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

# class SendSmsForm(forms.Form):
#     mobile_phone = forms.CharField(label='手机号',
#                                    validators=[RegexValidator(
#                                        r'^(1[3|4|5|6|7|8|9])\d{9}$',
#                                        '手机号样式错误错误'), ])
#     def __init__(self,request,*args,**kwargs):
#         super().__init__(*args,**kwargs)
#         self.request = request
#     def clean_mobile_phone(self):
#         '''校验是否注册'''
#         moblie_phone = self.cleaned_data['mobile_phone']
#         tpl = self.request.GET.get('tpl')
#         template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
#         #校验数据库种是否有这个手机号
#         if not template_id:
#             raise ValidationError('模板不存在')
#         exists = models.UserInfo.objects.filter(mobile_phone=moblie_phone).exists()
#         if exists:
#             raise ValidationError('手机号已存在')
#         code = random.randrange(1000,9999)
#         #发送短信
#         sms = send_sms_single(moblie_phone,template_id,[code,])
#         if sms['result'] != 0:
#             raise ValidationError(f"短信发送失败：{sms['errmsg']}")
#         #验证码写入redis(django-redis)
#         conn = get_redis_connection()
#         conn.set(moblie_phone,code,ex=60)
#         return moblie_phone

class SendSmsForm(forms.Form):
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(
        r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])

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
