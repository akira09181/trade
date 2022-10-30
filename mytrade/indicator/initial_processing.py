from ..models import Input
import datetime
import requests
from bs4 import BeautifulSoup


def data_get(request):
    ch = request.GET['candlestick']
    term_from_year = request.GET['term_from_year']
    term_from_month = request.GET['term_from_month']
    term_from_day = request.GET['term_from_day']
    term_to_year = request.GET['term_to_year']
    term_to_month = request.GET['term_to_month']
    term_to_day = request.GET['term_to_day']
    if int(term_from_month) < 10:
        term_from_month = '0'+term_from_month
    if int(term_from_day) < 10:
        term_from_day = '0'+term_from_day
    if int(term_to_month) < 10:
        term_to_month = '0'+term_to_month
    if int(term_to_day) < 10:
        term_to_day = '0'+term_to_day
    term_from = term_from_year+'-'+term_from_month+'-'+term_from_day
    term_to = term_to_year+'-'+term_to_month+'-'+term_to_day
    if ch == 'BTC1D':
        c = Input.objects.filter(
            date__gte=term_from, date__lte=term_to).values().order_by('date')
        print(c)
        lists = []
        for i in range(len(c)):
            li = [datetime.date(2020, 1, 1), 0, 0, 0, 0, 0]
            li[0] = c[i]['date']
            li[1] = c[i]['start']
            li[2] = c[i]['high']
            li[3] = c[i]['low']
            li[4] = c[i]['end']
            li[5] = c[i]['volume']
            lists.append(li)
    elif ch == 'BTC1H':
        response = requests.get(
            'http://nipper.work/btc/index.php?market=bitFlyer&coin=BTCJPY&periods=3600&after=1633072680')
        bs = BeautifulSoup(response.text, 'html.parser')
        value = bs.find_all('td')
        lists = []
        for i in range(int(len(value)/6)):
            li = []
            for j in range(6):
                li.append(value[i*6+j].get_text())
            lists.append(li)
            # c = InputHour.objects.all().values().order_by('date')
    elif ch == 'BTC4H':
        response = requests.get(
            'http://nipper.work/btc/index.php?market=bitFlyer&coin=BTCJPY&periods=14400&after=1593587880')
        bs = BeautifulSoup(response.text, 'html.parser')
        value = bs.find_all('td')
        lists = []
        for i in range(int(len(value)/6)):
            li = []
            for j in range(6):
                li.append(value[i*6+j].get_text())
            lists.append(li)
        # c = Btc4H.objects.all().values().order_by('date')
    elif ch == 'BTC5M':
        response = requests.get(
            'http://nipper.work/btc/index.php?market=bitFlyer&coin=BTCJPY&periods=300&after=1633072680')
        bs = BeautifulSoup(response.text, 'html.parser')
        value = bs.find_all('td')
        lists = []
        for i in range(int(len(value)/6)):
            li = []
            for j in range(6):
                li.append(value[i*6+j].get_text())
            lists.append(li)
        # c = Btc5M.objects.all().values().order_by('date')
    elif ch == 'BTC1M':
        response = requests.get(
            'http://nipper.work/btc/index.php?market=bitFlyer&coin=BTCJPY&periods=60&after=1633072680')
        bs = BeautifulSoup(response.text, 'html.parser')
        value = bs.find_all('td')
        lists = []
        for i in range(int(len(value)/6)):
            li = []
            for j in range(6):
                li.append(value[i*6+j].get_text())
            lists.append(li)

    return lists
