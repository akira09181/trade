from django import forms
from .models import Sma, Bre, Input
import datetime


class SmaForm(forms.ModelForm):

    candlestick = forms.fields.ChoiceField(choices=(
        ('BTC1D', 'BTC1日足'), ('BTC4H', 'BTC4時間足'), ('BTC1H',
                                                    'BTC1時間足'), ('BTC5M', 'BTC5分足'), ('BTC1M', 'BTC1分足')
    ), required=False)

    class Meta:
        year_from = Input.objects.all().values().order_by('date')
        model = Sma
        fields = ('__all__')
        datetime = datetime.datetime.now()
        date = datetime.date()
        year = date.strftime('%Y')
        print(year_from)
        widgets = {
            'term_from': forms.SelectDateWidget(),
            'term_to': forms.SelectDateWidget(),
        }

    def clean_term_from(self):
        term_from_year = self.cleaned_data.get('term_from_year')
        term_from_month = self.cleaned_data.get('term_from_month')
        if term_from_year == 2015 and term_from_month < 7:
            raise forms.ValidationError('2015年7月以降を選択してください。')
        return term_from_year


class BreForm(forms.ModelForm):

    candlestick = forms.fields.ChoiceField(choices=(
        ('BTC1D', 'BTC1日足'), ('BTC4H', 'BTC4時間足'), ('BTC1H',
                                                    'BTC1時間足'), ('BTC5M', 'BTC5分足'), ('BTC1M', 'BTC1分足')
    ), required=False)

    class Meta:
        model = Bre
        year_from = Input.objects.all().values().order_by('date')
        fields = ('__all__')
        datetime = datetime.datetime.now()
        date = datetime.date()
        year = date.strftime('%Y')
        widgets = {
            'term_from': forms.SelectDateWidget(),
            'term_to': forms.SelectDateWidget(),
        }
