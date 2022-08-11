from django import forms
from .models import Sma, Bre
import datetime


class SmaForm(forms.ModelForm):
    choice = forms.fields.ChoiceField(choices=(
        ('BTC1D', 'BTC1日足'), ('BTC4H', 'BTC4時間足'), ('BTC1H',
                                                    'BTC1時間足'), ('BTC5M', 'BTC5分足'), ('BTC1M', 'BTC1分足')
    ), required=False)

    class Meta:
        model = Sma
        fields = ('__all__')
        datetime = datetime.datetime.now()
        date = datetime.date()
        year = date.strftime('%Y')
        widgets = {
            'term_from': forms.SelectDateWidget(years=[x for x in range(2016, int(year))]),
            'term_to': forms.SelectDateWidget(years=[x for x in range(2016, int(year))]),
        }


class BreForm(forms.ModelForm):
    choice = forms.fields.ChoiceField(choices=(
        ('BTC1D', 'BTC1日足'), ('BTC4H', 'BTC4時間足'), ('BTC1H',
                                                    'BTC1時間足'), ('BTC5M', 'BTC5分足'), ('BTC1M', 'BTC1分足')
    ), required=False)

    class Meta:
        model = Bre

        fields = ('day', 'val', 'sjpy')
        datetime = datetime.datetime.now()
        date = datetime.date()
        year = date.strftime('%Y')
        widgets = {
            'term_from': forms.SelectDateWidget(years=[x for x in range(2016, int(year))]),
            'term_to': forms.SelectDateWidget(years=[x for x in range(2016, int(year))]),
        }
