from django.contrib import admin
from django.urls import path,include
from app01 import views
from web.views import account

urlpatterns = [
    # path('app01/send/sms/', views.send_sms),
    # path('app01/register/', views.register),
    path('register/', account.register,name='register'),
    path('send/sms/', account.send_sms,name='send_sms')

]