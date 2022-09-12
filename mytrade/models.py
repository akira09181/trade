from django.db import models
import datetime
from django.utils import timezone
# Create your models here.


class Users(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    adress = models.CharField(max_length=200)
    tell = models.CharField(max_length=20)
    register_date = models.DateTimeField('date published')
    last_in_date = models.DateTimeField('date published', null=True)


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
    term_from = models.DateField(default='2020-01-01', verbose_name='~から')
    term_to = models.DateField(default='2021-01-01', verbose_name='~まで')


class Bre(models.Model):
    day = models.IntegerField(default=20, verbose_name="移動平均線（足）")
    val = models.IntegerField(default=30, verbose_name="取引量（％）")
    sjpy = models.IntegerField(default=100000, verbose_name="初期の投資額")
    term_from = models.DateField(default='2020-01-01', verbose_name='~から')
    term_to = models.DateField(default='2021-01-01', verbose_name='~まで')


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


class Inquiry(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.CharField(max_length=1000, null=True)


class Records(models.Model):
    name = models.CharField(max_length=255)
    indicator = models.CharField(max_length=100)
    first_money = models.IntegerField()
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    result = models.IntegerField()
    times = models.FloatField(null=True)
