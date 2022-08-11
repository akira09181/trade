from django.db import models
from django import forms
import datetime
from django.utils import timezone
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

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date <= now


class InputHour(models.Model):
    date = models.DateTimeField(primary_key=True)
    start = models.IntegerField()
    high = models.IntegerField()
    low = models.IntegerField()
    end = models.IntegerField()
    volume = models.FloatField()


class Sma(models.Model):
    short = models.IntegerField(default=5, verbose_name="短い移動平均線")
    long = models.IntegerField(default=14, verbose_name="長い移動平均線")
    val = models.IntegerField(default=30, verbose_name="取引量（％）")
    sjpy = models.IntegerField(default=100000, verbose_name="初期の投資額")
    term_from = models.DateField()
    term_to = models.DateField()


class Bre(models.Model):
    day = models.IntegerField(default=20, verbose_name="移動平均線（足）")
    val = models.IntegerField(default=30, verbose_name="取引量（％）")
    sjpy = models.IntegerField(default=10, verbose_name="初期の投資額")


class Btc1M(models.Model):
    date = models.DateTimeField(primary_key=True)
    start = models.IntegerField()
    high = models.IntegerField()
    low = models.IntegerField()
    end = models.IntegerField()
    volume = models.FloatField()


class Btc5M(models.Model):
    date = models.DateTimeField(primary_key=True)
    start = models.IntegerField()
    high = models.IntegerField()
    low = models.IntegerField()
    end = models.IntegerField()
    volume = models.FloatField()


class Btc4H(models.Model):
    date = models.DateTimeField(primary_key=True)
    start = models.IntegerField()
    high = models.IntegerField()
    low = models.IntegerField()
    end = models.IntegerField()
    volume = models.FloatField()
