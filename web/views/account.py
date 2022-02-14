'''
用户相关功能
'''

from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from web.forms.account import RegisterModelForm,SendSmsForm


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
    form = SendSmsForm(request,data=request.GET)
    if form.is_valid():
        return JsonResponse({'status':True})
    return JsonResponse({'status':False,'error':form.errors})