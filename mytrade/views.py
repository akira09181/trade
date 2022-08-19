from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import math
from .models import Input, InputHour, Btc1M, Btc4H, Btc5M
from .forms import SmaForm, BreForm
import datetime


# Create your views here.
def index(request):

    response = requests.get(
        'http://nipper.work/btc/index.php?market=bitFlyer&coin=BTCJPY&periods=86400&after=1420070400')
    bs = BeautifulSoup(response.text, "html.parser")
    value = bs.find_all("td")
    lists = []
    num = int(len(value)/6)
    n = 0
    for i in range(int(len(value)/6)):
        li = []
        for j in range(6):
            li.append(value[-(i*6+j)-1].get_text())
        lists.append(li)
        n = Input.objects.filter(date=li[5][:10]).count()
        if n == 1:
            break
        c = Input(date=li[5][:10], start=int(li[4]), high=int(
            li[3]), low=int(li[2]), end=int(li[1]), volume=float(li[0]))

        c.save()
    d = Input.objects.all().values().order_by('date')

    context = {"value": d, "num": num, "BreForm": BreForm, "SmaForm": SmaForm}
    return render(request, "mytrade/index.html", context)


def sma(request):
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
        print(c[0])
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
        #c = InputHour.objects.all().values().order_by('date')
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
        #c = Btc4H.objects.all().values().order_by('date')
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
        #c = Btc5M.objects.all().values().order_by('date')
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
        #c = Btc1M.objects.all().values().order_by('date')
    short = request.GET["short"]
    long = request.GET["long"]
    val = request.GET["val"]

    sh = int(short)
    lo = int(long)
    va = int(val)/100
    trandflag = 0
    avl = 0
    avs = 0

    sjpy = int(request.GET['sjpy'])
    jpy = sjpy
    bitcoin = 0
    buycoin = 0
    buyjpy = 0
    result = [["", 0, 0]for i in range(len(lists))]
    for i in range(len(lists)):
        avl = 0
        avs = 0
        if i >= lo:
            for j in range(lo):
                avl += int(lists[i-j][1])
            avl /= lo
            for j in range(sh):
                avs += int(lists[i-j][1])
            avs /= sh
        if avl < avs and trandflag == 0:
            trandflag = 1
            buycoin = jpy*va
            jpy -= buycoin
            bitcoin += buycoin/int(lists[i][1])
        elif avl > avs and trandflag == 1:
            trandflag = 0
            buyjpy = bitcoin*va
            bitcoin -= bitcoin*va
            jpy += buyjpy * int(lists[i][1])
        result[i][0] = lists[i][0]
        result[i][1] = jpy
        result[i][2] = bitcoin
    resultend = int(bitcoin*int(lists[len(lists)-1][1])+jpy)
    bai = resultend/sjpy
    jpy = int(jpy)
    context = {"result": result, "resultjpy": jpy,
               "resultcoin": bitcoin, "resultend": resultend, "bai": bai}
    return render(request, "mytrade/sma.html", context)


def breverse(request):
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
        print(c[0])
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
        #c = InputHour.objects.all().values().order_by('date')
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
        #c = Btc4H.objects.all().values().order_by('date')
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
        #c = Btc5M.objects.all().values().order_by('date')
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
        #c = Btc1M.objects.all().values().order_by('date')
    response = requests.get(
        'http://nipper.work/btc/index.php?market=bitFlyer&coin=BTCJPY&periods=86400&after=1420070400')
    bs = BeautifulSoup(response.text, "html.parser")
    value = bs.find_all("td")
    lists = []
    for i in range(int(len(value)/6)):
        li = []
        for j in range(6):

            li.append(value[i*6+j].get_text())
        if li[1] != "0":
            lists.append(li)
    day = request.GET["day"]
    val = request.GET["val"]
    da = int(day)
    va = int(val)/100
    sjpy = int(request.GET['sjpy'])
    jpy = sjpy
    ave = 0
    dtb = 0
    bitcoin = 0
    buycoin = 0
    buyjpy = 0

    result = [["", 0, 0]for i in range(len(lists))]
    for i in range(len(lists)):
        if i > da:
            ave = 0
            for j in range(da):
                ave += int(lists[i-j][1])
            ave /= da
            dtb = 0
            for j in range(da):
                dtb += (int(lists[i-j][1])-ave)**2
            dtb /= da

            dtb = math.sqrt(dtb)

            if int(lists[i][3]) < ave-dtb*2 and lists[i][1] != 0:
                buycoin = jpy*va
                jpy -= buycoin
                bitcoin += buycoin/(ave-dtb*2)
            elif int(lists[i][2]) > ave+dtb*2 and lists[i][1] != 0:
                buyjpy = bitcoin*va
                bitcoin -= buyjpy
                jpy += buyjpy*(ave+dtb*2)
        result[i][0] = lists[i][0]
        result[i][1] = jpy
        result[i][2] = bitcoin
    resultend = int(bitcoin*int(lists[len(c)-1][1])+jpy)
    bai = resultend/sjpy
    jpy = int(jpy)
    context = {"resultend": resultend, "result": result,
               "resultjpy": jpy, "resultcoin": bitcoin, "bai": bai}
    return render(request, "mytrade/breverse.html", context)


def bbreak(request):
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
    elif ch == 'BTC1H':
        c = InputHour.objects.all().values().order_by('date')
    elif ch == 'BTC4H':
        c = Btc4H.objects.all().values().order_by('date')
    elif ch == 'BTC5M':
        c = Btc5M.objects.all().values().order_by('date')
    elif ch == 'BTC1M':
        c = Btc1M.objects.all().values().order_by('date')
    response = requests.get(
        'http://nipper.work/btc/index.php?market=bitFlyer&coin=BTCJPY&periods=86400&after=1420070400')
    bs = BeautifulSoup(response.text, "html.parser")
    value = bs.find_all("td")
    lists = []
    for i in range(int(len(value)/6)):
        li = []
        for j in range(6):

            li.append(value[i*6+j].get_text())
        if li[1] != "0":
            lists.append(li)
    day = request.GET["day"]
    val = request.GET["val"]
    da = int(day)
    va = int(val)/100
    sjpy = int(request.GET['sjpy'])
    jpy = sjpy
    ave = 0
    dtb = 0
    bitcoin = 0
    buycoin = 0
    buyjpy = 0
    countbuy = 0
    countsell = 0

    result = [["", 0, 0]for i in range(len(c))]
    for i in range(len(c)):
        ave = 0
        dtb = 0
        if i > da:
            for j in range(da):
                ave += int(c[i-j]['start'])
            ave /= da
            for j in range(da):
                dtb += (int(c[i-j]['start'])-ave)**2
            dtb /= da

            dtb = math.sqrt(dtb)
            if int(c[i]['start']) > ave+2*dtb:
                buycoin = jpy*va
                jpy -= buycoin
                bitcoin += buycoin/int(c[i]['start'])
                countbuy += 1
            elif int(c[i]['start']) < ave-2*dtb:
                buyjpy = bitcoin*va
                bitcoin -= buyjpy
                jpy += buyjpy*int(c[i]['start'])
                countsell += 1
        result[i][0] = c[i]['date']
        result[i][1] = jpy
        result[i][2] = bitcoin
    resultend = int(bitcoin*int(c[len(c)-1]['start'])+jpy)
    bai = resultend/sjpy
    jpy = int(jpy)
    context = {"resultend": resultend, "result": result, "resultjpy": jpy, "resultcoin": bitcoin, "bai": bai,
               "countbuy": countbuy, "countsell": countsell}
    return render(request, "mytrade/result.html", context)


def macd(request):
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
    elif ch == 'BTC1H':
        c = InputHour.objects.all().values().order_by('date')
    elif ch == 'BTC4H':
        c = Btc4H.objects.all().values().order_by('date')
    elif ch == 'BTC5M':
        c = Btc5M.objects.all().values().order_by('date')
    elif ch == 'BTC1M':
        c = Btc1M.objects.all().values().order_by('date')
    response = requests.get(
        'http://nipper.work/btc/index.php?market=bitFlyer&coin=BTCJPY&periods=86400&after=1420070400')
    bs = BeautifulSoup(response.text, "html.parser")
    value = bs.find_all("td")
    lists = []
    for i in range(int(len(value)/6)):
        li = []
        for j in range(6):
            li.append(value[i*6+j].get_text())
        lists.append(li)
    short = request.GET["short"]
    long = request.GET["long"]
    val = request.GET["val"]
    sh = int(short)
    lo = int(long)
    va = int(val)/100
    trandflag = 0
    avl = 0
    avs = 0
    sjpy = int(request.GET['sjpy'])
    jpy = sjpy
    bitcoin = 0
    buycoin = 0
    buyjpy = 0
    result = [["", 0, 0]for i in range(len(c))]
    for i in range(len(c)):
        avl = 0
        avs = 0
        countl = 0
        counts = 0
        if i >= lo:
            for j in range(lo):
                avl += int(c[i-j]['start'])*(lo-j)
                countl += (lo-j)
            avl /= countl
            for j in range(sh):
                avs += int(c[i-j]['start'])*(sh-j)
                counts += (sh-j)
            avs /= counts
        if avl < avs and trandflag == 0:
            trandflag = 1
            buycoin = jpy*va
            jpy -= buycoin
            bitcoin += buycoin/int(c[i]['start'])
        if avl > avs and trandflag == 1:
            trandflag = 0
            buyjpy = bitcoin*va
            bitcoin -= bitcoin*va
            jpy += buyjpy * int(c[i]['start'])
        result[i][0] = c[i]['date']
        result[i][1] = jpy
        result[i][2] = bitcoin
    resultend = int(bitcoin*int(c[len(c)-1]['start'])+jpy)
    bai = resultend/sjpy
    jpy = int(jpy)
    context = {"result": result, "resultjpy": jpy,
               "resultcoin": bitcoin, "resultend": resultend, "bai": bai}
    return render(request, "mytrade/result.html", context)


def results(request):
    return HttpResponse("This is result")


def rsi(request):
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
    elif ch == 'BTC1H':
        c = InputHour.objects.all().values().order_by('date')
    elif ch == 'BTC4H':
        c = Btc4H.objects.all().values().order_by('date')
    elif ch == 'BTC5M':
        c = Btc5M.objects.all().values().order_by('date')
    elif ch == 'BTC1M':
        c = Btc1M.objects.all().values().order_by('date')
    day = int(request.GET['day'])
    val = int(request.GET['val'])/100
    sjpy = int(request.GET['sjpy'])
    jpy = sjpy
    coin = 0
    plus = 0
    minus = 0
    rsi = 0
    buyjpy = 0
    buycoin = 0
    result = [["", 0, 0]for i in range(len(c))]
    countbuy = 0
    countsell = 0
    for i in range(len(c)):
        minus = 0
        plus = 0
        if i > day:
            for j in range(day):
                a = int(c[i-j-1]['start'])-int(c[i-j]['start'])
                if a < 0:
                    minus -= a
                else:
                    plus += a
            minus /= day
            plus /= day
            rsi = plus/(plus+minus)*100
            if rsi < 30:
                buycoin = jpy*val
                jpy -= buycoin
                coin += buycoin/int(c[i]['start'])
                countbuy += 1
            if rsi > 70:
                buyjpy = coin*val
                jpy += buyjpy*int(c[i]['start'])
                coin -= buyjpy
                countsell += 1
        result[i][0] = c[i]['date']
        result[i][1] = jpy
        result[i][2] = coin
    end = int(jpy+coin*(c[len(c)-1]['start']))
    bai = end/sjpy
    context = {'result': result, 'resultend': end, 'bai': bai, 'resultjpy': jpy,
               'resultcoin': coin, 'countbuy': countbuy, 'countsell': countsell}
    return render(request, "mytrade/result.html", context)


def fib(request):
    day = int(request.GET['day'])
    val = int(request.GET['val'])/100
    sjpy = int(request.GET['sjpy'])
    jpy = sjpy
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
    elif ch == 'BTC1H':
        c = InputHour.objects.all().values().order_by('date')
    elif ch == 'BTC4H':
        c = Btc4H.objects.all().values().order_by('date')
    elif ch == 'BTC5M':
        c = Btc5M.objects.all().values().order_by('date')
    elif ch == 'BTC1M':
        c = Btc1M.objects.all().values().order_by('date')
    coin, buyjpy, buycoin, countbuy, countsell, rsi, trand = 0, 0, 0, 0, 0, 0, 0
    minus, plus = 0, 0
    result = [["", 0, 0]for i in range(len(c))]
    high, low = [], []
    for i in range(len(c)):
        minus = 0
        plus = 0
        high, low = [], []
        if i > day:
            for j in range(day):
                a = c[i-j-1]['start']-c[i-j]['start']
                if a < 0:
                    minus -= a
                else:
                    plus += a
            minus /= day
            plus /= day
            rsi = plus/(plus+minus)*100

            for j in range(day):
                high.append(c[i-j]['high'])
                if c[i-j]['low'] != 0:
                    low.append(c[i-j]['low'])
            high.sort()
            low.sort()
            h = high[-1]
            l = low[0]
            min = (h-l)*0.236+l
            min2 = (h-l)*0.382+l
            mid = (h-l)*0.5+l
            max2 = (h-l)*0.618+l
            max = (h-l)*0.784+l
            hh = (h-l)*1.618+l
            h2 = (h-l)*1.382+l
            hm = (h-l)*1.5+l
            if rsi > 70:
                buyjpy = coin*val
                coin -= buyjpy
                jpy += buyjpy*c[i]['start']
                countsell += 1
            elif rsi < 30:
                buycoin = jpy*val
                jpy -= buycoin
                coin += buycoin/c[i]['start']
                countbuy += 1
            elif rsi > 50:
                if c[i]['low'] < min and c[i]['low'] != 0:
                    buycoin = jpy*val
                    jpy -= buycoin
                    coin += buycoin/min
                    countbuy += 1
                if c[i]['high'] > mid:
                    buyjpy = coin*val
                    coin -= buyjpy
                    jpy += buyjpy*mid
                    countsell += 1

            else:
                if c[i]['low'] < mid and c[i]['low'] != 0:
                    buycoin = jpy*val
                    jpy -= buycoin
                    coin += buycoin/mid
                    countbuy += 1
                if c[i]['high'] > max:
                    buyjpy = coin*val
                    coin -= buyjpy
                    jpy += buyjpy*max
                    countsell += 1

        result[i][0] = c[i]['date']
        result[i][1] = jpy
        result[i][2] = coin
    end = int(coin*c[len(c)-1]['start']+jpy)
    bai = end/sjpy
    jpy = int(jpy)

    context = {'resultjpy': jpy, 'resultcoin': coin, 'countbuy': countbuy,
               'countsell': countsell, 'result': result, 'bai': bai, 'resultend': end}
    return render(request, "mytrade/result.html", context)


def st(request):
    day = int(request.GET['day'])
    val = int(request.GET['val'])/100
    sjpy = int(request.GET['sjpy'])
    jpy = sjpy
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
    elif ch == 'BTC1H':
        c = InputHour.objects.all().values().order_by('date')
    elif ch == 'BTC4H':
        c = Btc4H.objects.all().values().order_by('date')
    elif ch == 'BTC5M':
        c = Btc5M.objects.all().values().order_by('date')
    elif ch == 'BTC1M':
        c = Btc1M.objects.all().values().order_by('date')
    result = [["", 0, 0]for i in range(len(c))]
    h = 0
    l = 1000000000000000
    k, d, b, e = 0, 0, 0, 0
    bf, sf = 0, 0
    coin = 0
    cb, cs = 0, 0
    for i in range(len(c)):
        h = 0
        l = 1000000000000000
        b, e = 0, 0
        if i > day+3:
            for j in range(day):
                if h < c[i-j]['high']:
                    h = c[i-j]['high']
                if l > c[i-j]['low']:
                    l = c[i-j]['low']
            k = (c[i-1]['end']-l)/(h-l)*100
            for j in range(3):
                h = 0
                l = 1000000000000000
                for m in range(day):
                    if h < c[i-m-j]['high']:
                        h = c[i-m]['high']
                    if l > c[i-m-j]['low'] and c[i-m-j]['low'] != 0:
                        l = c[i-j-m]['low']
                b += h-l
                e += c[i-j-1]['end']-l
            d = e/b*100
            if k < 20 and d < 20 and k < d:
                bf = 1
            elif k > 80 and d > 80 and k > d:
                sf = 1
            elif k < 20 and d < 20 and k > d and bf == 1:
                coin += (jpy*val)/c[i]['start']
                jpy -= jpy*val
                bf = 0
                cb += 1
            elif k > 80 and d > 80 and k < d and sf == 1:
                jpy += coin*val*c[i]['start']
                coin -= coin*val
                sf = 0
                cs += 1
            else:
                bf = 0
                sf = 0
        result[i][0] = c[i]['date']
        result[i][1] = jpy
        result[i][2] = coin
    jpy = int(jpy)
    resultjpy = int(coin*c[len(c)-1]['start'])+jpy
    bai = resultjpy/sjpy

    context = {'resultjpy': jpy, 'resultcoin': coin, 'resultend': resultjpy,
               'bai': bai, 'countbuy': cb, 'countsell': cs, 'result': result}
    return render(request, 'mytrade/result.html', context)


def hour(request):
    # HEROKUの無料分を越えてしまうため、短いローソク足はカットしている。
    k = 0
    if k == 1:
        response = requests.get(
            'http://nipper.work/btc/index.php?market=bitFlyer&coin=BTCJPY&periods=3600&after=1633072680')
        bs = BeautifulSoup(response.text, 'html.parser')
        value = bs.find_all('td')
        n = 0
        for i in range(int(len(value)/6)):
            b = value[(-i-1)*6].get_text()
            a = datetime.datetime.strptime(b, "%Y-%m-%d %H:%M:%S")
            c = InputHour(date=a, start=int(value[(-i-1)*6+1].get_text()), high=int(value[(-i-1)*6+2].get_text()), low=int(
                value[(-i-1)*6+3].get_text()), end=int(value[(-i-1)*6+4].get_text()), volume=float(value[(-i-1)*6+5].get_text()))
            n = InputHour.objects.filter(date=a).count()
            if n == 1:
                pass
            else:
                c.save()
    if k == 1:
        response = requests.get(
            'http://nipper.work/btc/index.php?market=bitFlyer&coin=BTCJPY&periods=60&after=1633072680')
        bs = BeautifulSoup(response.text, 'html.parser')
        value = bs.find_all('td')
        n = 0
        for i in range(int(len(value)/6)):
            b = value[(-i-1)*6].get_text()
            a = datetime.datetime.strptime(b, "%Y-%m-%d %H:%M:%S")
            n = Btc1M.objects.filter(date=a).count()
            if n == 1:
                break
            c = Btc1M(date=a, start=int(value[(-i-1)*6+1].get_text()), high=int(value[(-i-1)*6+2].get_text()), low=int(
                value[(-i-1)*6+3].get_text()), end=int(value[(-i-1)*6+4].get_text()), volume=float(value[(-i-1)*6+5].get_text()))
            c.save()
    if k == 1:
        response = requests.get(
            'http://nipper.work/btc/index.php?market=bitFlyer&coin=BTCJPY&periods=300&after=1633072680')
        bs = BeautifulSoup(response.text, 'html.parser')
        value = bs.find_all('td')
        n = 0
        for i in range(int(len(value)/6)):
            b = value[(-i-1)*6].get_text()
            a = datetime.datetime.strptime(b, "%Y-%m-%d %H:%M:%S")
            n = Btc5M.objects.filter(date=a).count()
            if n == 1:
                break
            c = Btc5M(date=a, start=int(value[(-i-1)*6+1].get_text()), high=int(value[(-i-1)*6+2].get_text()), low=int(
                value[(-i-1)*6+3].get_text()), end=int(value[(-i-1)*6+4].get_text()), volume=float(value[(-i-1)*6+5].get_text()))
            c.save()
        response = requests.get(
            'http://nipper.work/btc/index.php?market=bitFlyer&coin=BTCJPY&periods=14400&after=1593587880')
        bs = BeautifulSoup(response.text, 'html.parser')
        value = bs.find_all('td')
        n = 0
        for i in range(int(len(value)/6)):
            b = value[(-i-1)*6].get_text()
            a = datetime.datetime.strptime(b, "%Y-%m-%d %H:%M:%S")
            n = Btc4H.objects.filter(date=a).count()
            if n == 1:
                break
            c = Btc4H(date=a, start=int(value[(-i-1)*6+1].get_text()), high=int(value[(-i-1)*6+2].get_text()), low=int(
                value[(-i-1)*6+3].get_text()), end=int(value[(-i-1)*6+4].get_text()), volume=float(value[(-i-1)*6+5].get_text()))
            c.save()
    d = Btc1M.objects.all().values().order_by('date')
    context = {'value': d, 'BreForm': BreForm, "SmaForm": SmaForm}
    return render(request, 'mytrade/index.html', context)
