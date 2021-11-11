from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name = 'index'),
    path('results',views.results,name='results'),
    path('sma',views.sma,name="sma"),
    path('breverse',views.breverse,name="breverse"),
]