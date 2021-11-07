from django.db import models

# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=200) 
    password = models.CharField(max_length=200)
    adress = models.CharField(max_length=200)
    tell = models.CharField(max_length=20)
    register_date = models.DateTimeField('date published')
    last_in_date = models.DateTimeField('date published')