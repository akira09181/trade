from django.urls import path
from .views import views, views_get_xrp_data

urlpatterns = [
    path('', views.index, name='index'),
    path('results', views.results, name='results'),
    path('sma', views.sma, name="sma"),
    path('breverse', views.breverse, name="breverse"),
    path('bbreak', views.bbreak, name="bbreak"),
    path('macd', views.macd, name='macd'),
    path('rsi', views.rsi, name='rsi'),
    path('fib', views.fib, name="fib"),
    path('st', views.st, name='st'),
    path('hour', views.hour, name='hour'),
    path('inquiry', views.inquiry, name='inquiry'),
    path('pre_inquiry', views.pre_inquiry, name='pre_inquiry'),
    path('register', views.register, name='register'),
    path('pre_register', views.pre_register, name='pre_register'),
    path('login', views.login, name='login'),
    path('pre_login', views.pre_login, name='pre_login'),
    path('mypage', views.mypage, name='mypage'),
    path('get_xrp', views_get_xrp_data.get_xrp, name='get_xrp')
]
