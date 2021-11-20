from django.db import models
from django import forms
# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=200) 
    password = models.CharField(max_length=200)
    adress = models.CharField(max_length=200)
    tell = models.CharField(max_length=20)
    register_date = models.DateTimeField('date published')
    last_in_date = models.DateTimeField('date published')
    
class Input(models.Model):
    date = models.DateField(primary_key=True)
    start = models.IntegerField()
    high = models.IntegerField()
    low = models.IntegerField()
    end = models.IntegerField()
    volume = models.FloatField()

class Sma(models.Model):
    short = models.IntegerField(default=5,verbose_name="短い移動平均線")
    long = models.IntegerField(default=14,verbose_name="長い移動平均線")
    val = models.IntegerField(default=30,verbose_name="取引量（％）")
    sjpy = models.IntegerField(default=100000,verbose_name="初期の投資額")
        
class Bre(models.Model):
    day = models.IntegerField(default=20,verbose_name="移動平均線（日）")
    val = models.IntegerField(default=30,verbose_name="取引量（％）")
    sjpy = models.IntegerField(default=100000,verbose_name="初期の投資額")
