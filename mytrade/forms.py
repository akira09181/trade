from django import forms
from .models import Sma,Bre

class SmaForm(forms.ModelForm):
    class Meta:
        model=Sma
        fields = ('short','long','val','sjpy')

class BreForm(forms.ModelForm):
    class Meta:
        model=Bre
        fields = ('day','val','sjpy')