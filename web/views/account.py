'''
用户相关功能
'''

from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse

from web import models
from web.forms.account import RegisterModelForm,SendSmsForm,LoginSMSForm,LoginForm

from utils.image_code import check_code
from io import BytesIO

def register(request):
    if request.method == 'GET':
        form =RegisterModelForm()
        return render(request,'register.html',{'form':form})
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        #验证通过，写入数据库
        form.save()
        return JsonResponse({'status':True,'data':'/login/'})

    return JsonResponse({'status':False,'error':form.errors})

def send_sms(request):
    """发送短信"""
    form = SendSmsForm(request, data=request.GET)
    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def login_sms(request):
    '''短信登录'''
    if request.method == 'GET':
        form = LoginSMSForm()
        return render(request,'login_sms.html',{'form':form})
    print(request.POST)
    form = LoginSMSForm(request.POST)
    if form.is_valid():
        # user_object = form.cleaned_data['mobile_phone']
        # #存放用户session
        # print(user_object)
        moblie_phone = form.cleaned_data['mobile_phone']
        user_object = models.UserInfo.objects.filter(mobile_phone=moblie_phone).first()
        request.session['user_id'] = user_object.id
        request.session['use_name'] = user_object.username
        return JsonResponse({'status': True,'data':'/index/'})
    return JsonResponse({'status': False, 'error': form.errors})


def login(request):
    '''用户名和密码登录'''
    if request.method == "GET":
        form = LoginForm()
        return render(request,'login.html',{'form':form})
    form =  LoginForm(data = request.POST)
    if form.is_valid():
        return redirect('index')
    return render(request,'login.html',{'form':form})


def image_code(request):
    '''生成图片验证码'''

    image_object,code= check_code()
    request.session['image_code'] = code
    request.session.set_expiry(60)

    stream = BytesIO()
    image_object.save(stream,'png')

    return HttpResponse(stream.getvalue())

