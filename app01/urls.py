from django.contrib import admin
from django.urls import path
from app01 import views
from web.views import account

urlpatterns = [
    # path('app01/send/sms/', views.send_sms),
    # path('app01/register/', views.register),
    path('register/', views.register)

]