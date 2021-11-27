from django import forms
from .models import Sma,Bre

class SmaForm(forms.ModelForm):
    choice = forms.fields.ChoiceField(choices = (
        ('BTC1D','BTC1日足'),('BTC4H','BTC4時間足'),('BTC1H','BTC1時間足'),('BTC5M','BTC5分足'),('BTC1M','BTC1分足')
        ),required=False)
    class Meta:
        model=Sma
        fields = ('short','long','val','sjpy')

class BreForm(forms.ModelForm):
    choice = forms.fields.ChoiceField(choices = (
        ('BTC1D','BTC1日足'),('BTC4H','BTC4時間足'),('BTC1H','BTC1時間足'),('BTC5M','BTC5分足'),('BTC1M','BTC1分足')
        ),required=False)
    class Meta:
        model=Bre
        
        fields = ('day','val','sjpy')