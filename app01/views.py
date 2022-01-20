from django.shortcuts import render,HttpResponse

# Create your views here.
from utils.tencent.sms import send_sms_single
import random

from django.conf import settings

def send_sms(request):
    '''
    ?tlp=register -》1283745
    '''
    code = random.randrange(1000, 9999)
    tpl = request.GET.get('tpl')
    template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
    userPhoneNum = 15882887813
    if not template_id:
        return HttpResponse('模板不存在')
    res = send_sms_single(userPhoneNum,template_id,[code,])
    print(res)
    if res['result'] == 0:
        return HttpResponse('成功')
    else:
        return HttpResponse(res['errmsg'])