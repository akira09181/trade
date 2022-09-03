from django.urls import path
from . import views

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
]
