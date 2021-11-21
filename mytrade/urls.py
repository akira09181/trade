from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name = 'index'),
    path('results',views.results,name='results'),
    path('sma',views.sma,name="sma"),
    path('breverse',views.breverse,name="breverse"),
    path('bbreak',views.bbreak,name="bbreak"),
    path('macd',views.macd,name='macd'),
    path('rsi',views.rsi,name='rsi'),
]