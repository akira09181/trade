from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string

import requests
import datetime
from bs4 import BeautifulSoup
import math

import json

from ..models import Input, InputHour, Btc1M, Btc4H, Btc5M, Users, Records
from ..forms import SmaForm, BreForm, Inquiry, Register, Login, Ifd
from ..indicator.initial_processing import data_get


# Create your views here.
def index(request):
    login_ok = request.GET.get('login_ok')
    name = request.GET.get('name')
    endPoint = 'https://api.coin.z.com/public'
    path = '/v1/klines?symbol=BTC&interval=1day&date=2023'

    response = requests.get(endPoint + path).json()

    print(datetime.datetime.utcfromtimestamp(
        int(response['data'][0]['openTime'])/1000))

    data = response['data']
    print(data)
    for i in data:
        date = datetime.datetime.utcfromtimestamp(int(i['openTime'])/1000)
        c = Input(date=date, start=int(i['open']), high=int(i['high']), low=int(
            i['low']), end=int(i['close']), volume=float(i['volume']))

        c.save()
    d = Input.objects.all().values().order_by('date')
    '''
    response = requests.get(
        'http://nipper.work/btc/index.php?market=bitFlyer&coin=BTCJPY&periods=86400&after=1420070400')
    bs = BeautifulSoup(response.text, "html.parser")
    value = bs.find_all("td")
    lists = []
    num = int(len(value)/6
    n = 0
    for i in range(int(len(value)
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
    '''
    context = {"value": d, "BreForm": BreForm,
               "SmaForm": SmaForm, "login_ok": login_ok, 'name': name, "IfdForm": Ifd}

    return render(request, "mytrade/index.html", context)


def ifd_order(request):
    def __init__(self):
        orders = []
    lists = data_get(request)
    start_yen = int(request.GET['sjpy'])
    trade_value = start_yen/10
    jpy = start_yen
    btc = 0
    expire = int(request.GET['minute_to_expire'])/1440
    buy_order = int(request.GET['buy_order'])/100
    sell_order = int(request.GET['sell_order'])/100
    orders = [[0, 0, 0, 0, 0]for i in range(30)]
    del_flag = []
    result = [["", 0, 0, 0, 0, 0, 0, []]for i in range(len(lists))]
    bitcoin = 0

    for i in range(len(lists)):
        order_count = 0
        buy = int(lists[i][1])*buy_order
        sell = int(lists[i][1])*sell_order
        if jpy >= trade_value:
            jpy -= trade_value
        for j in range(len(orders)):
            if orders[j][0] == 0:
                orders[j] = [buy, sell, -1, 0, 0]
                order_count += 1
                break

        for j in range(len(orders)):
            if orders[j][0] != 0:
                orders[j][4] += 1
            if orders[j][4] > expire:
                del_flag.append(j)
                order_count -= 1
                if orders[j][2] == -1:
                    jpy += trade_value
                else:
                    jpy += orders[j][3]*lists[i][1]*0.9985
                    btc -= orders[j][3]
            else:
                if orders[j][2] == -1:
                    if orders[j][0] > int(lists[i][3]):
                        btc = trade_value/orders[j][0]
                        orders[j][3] = btc*0.9985
                        orders[j][2] = 1
                        bitcoin += btc
                else:
                    if orders[j][1] < int(lists[i][2]):
                        jpy += orders[j][3] * orders[j][1]*0.9985
                        del_flag.append(j)
                        order_count -= 1
                        bitcoin -= orders[j][3]
        if del_flag:
            if del_flag == [0]:
                del orders[0]
            else:
                for j in range(len(del_flag)):
                    del orders[del_flag[-j-1]]
            del_flag = []
        record_order = orders
        result[i][0] = lists[i][0]
        result[i][1] = jpy
        result[i][2] = bitcoin
        result[i][3] = lists[i][1]
        result[i][4] = lists[i][2]
        result[i][5] = lists[i][3]
        result[i][6] = order_count*trade_value+jpy+(btc*lists[i][1])
        result[i][7] = record_order
    for i in range(len(orders)):
        if orders[i][2] == 0:
            jpy += trade_value
    resultend = jpy+bitcoin*lists[-1][1]
    bai = resultend/start_yen
    context = {'result': result, 'resultjpy': jpy,
               'resultcoin': bitcoin, 'resultend': resultend, 'bai': bai}
    return render(request, "mytrade/result.html", context)


def sma(request):
    lists = data_get(request)
    sh = int(request.GET["short"])
    lo = int(request.GET["long"])
    va = int(request.GET["val"])/100
    sjpy = int(request.GET['sjpy'])
    login_ok = request.GET.get('login_ok')
    name = request.GET.get('name')
    jpy = sjpy
    trandflag = 0
    avl = 0
    avs = 0
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
    if login_ok:
        record = Records(name=name, indicator='SMA', first_money=sjpy,
                         from_date=lists[0][0], to_date=lists[-1][0], result=resultend, times=bai)
        record.save()
    context = {"result": result, "resultjpy": jpy,
               "resultcoin": bitcoin, "resultend": resultend, "bai": bai, "name": name, "login_ok": login_ok}
    return render(request, "mytrade/sma.html", context)


def breverse(request):
    lists = data_get(request)
    day = request.GET["day"]
    val = request.GET["val"]
    da = int(day)
    va = int(val)/100
    sjpy = int(request.GET['sjpy'])
    login_ok = request.GET.get('login_ok')
    name = request.GET.get('name')
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
    resultend = int(bitcoin*int(lists[len(lists)-1][1])+jpy)
    bai = resultend/sjpy
    jpy = int(jpy)
    if login_ok:
        record = Records(name=name, indicator='Bollinger_Bands_Contrary', first_money=sjpy,
                         from_date=lists[0][0], to_date=lists[-1][0], result=resultend, times=bai)
        record.save()
    context = {"resultend": resultend, "result": result,
               "resultjpy": jpy, "resultcoin": bitcoin, "bai": bai, "login_ok": login_ok, "name": name}
    return render(request, "mytrade/breverse.html", context)


def bbreak(request):
    lists = data_get(request)
    da = int(request.GET["day"])
    va = int(request.GET["val"])/100
    sjpy = int(request.GET['sjpy'])
    login_ok = request.GET.get('login_ok')
    name = request.GET.get('name')
    jpy = sjpy
    ave = 0
    dtb = 0
    bitcoin = 0
    buycoin = 0
    buyjpy = 0
    countbuy = 0
    countsell = 0
    result = [["", 0, 0]for i in range(len(lists))]
    for i in range(len(lists)):
        ave = 0
        dtb = 0
        if i > da:
            for j in range(da):
                ave += int(lists[i-j][1])
            ave /= da
            for j in range(da):
                dtb += (int(lists[i-j][1])-ave)**2
            dtb /= da

            dtb = math.sqrt(dtb)
            if int(lists[i][1]) > ave+2*dtb:
                buycoin = jpy*va
                jpy -= buycoin
                bitcoin += buycoin/int(lists[i][1])
                countbuy += 1
            elif int(lists[i][1]) < ave-2*dtb:
                buyjpy = bitcoin*va
                bitcoin -= buyjpy
                jpy += buyjpy*int(lists[i][1])
                countsell += 1
        result[i][0] = lists[i][0]
        result[i][1] = jpy
        result[i][2] = bitcoin
    resultend = int(bitcoin*int(lists[len(lists)-1][1])+jpy)
    bai = resultend/sjpy
    jpy = int(jpy)
    if login_ok:
        record = Records(name=name, indicator='Bollinger_Bands_Break_Out', first_money=sjpy,
                         from_date=lists[0][0], to_date=lists[-1][0], result=resultend, times=bai)
        record.save()
    context = {"resultend": resultend, "result": result, "resultjpy": jpy, "resultcoin": bitcoin,
               "bai": bai, "countbuy": countbuy, "countsell": countsell, "login_ok": login_ok, "name": name}
    return render(request, "mytrade/result.html", context)


def macd(request):
    lists = data_get(request)
    short = request.GET["short"]
    long = request.GET["long"]
    val = request.GET["val"]
    login_ok = request.GET.get('login_ok')
    name = request.GET.get('name')
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
        countl = 0
        counts = 0
        if i >= lo:
            for j in range(lo):
                avl += int(lists[i-j][1])*(lo-j)
                countl += (lo-j)
            avl /= countl
            for j in range(sh):
                avs += int(lists[i-j][1])*(sh-j)
                counts += (sh-j)
            avs /= counts
        if avl < avs and trandflag == 0:
            trandflag = 1
            buycoin = jpy*va
            jpy -= buycoin
            bitcoin += buycoin/int(lists[i][1])
        if avl > avs and trandflag == 1:
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
    if login_ok:
        record = Records(name=name, indicator='MACD', first_money=sjpy,
                         from_date=lists[0][0], to_date=lists[-1][0], result=resultend, times=bai)
        record.save()
    context = {"result": result, "resultjpy": jpy,
               "resultcoin": bitcoin, "resultend": resultend, "bai": bai, "login_ok": login_ok, "name": name}
    return render(request, "mytrade/result.html", context)


def results(request):
    return HttpResponse("This is result")


def rsi(request):
    lists = data_get(request)
    day = int(request.GET['day'])
    val = int(request.GET['val'])/100
    sjpy = int(request.GET['sjpy'])
    login_ok = request.GET.get('login_ok')
    name = request.GET.get('name')
    jpy = sjpy
    coin = 0
    plus = 0
    minus = 0
    rsi = 0
    buyjpy = 0
    buycoin = 0
    result = [["", 0, 0]for i in range(len(lists))]
    countbuy = 0
    countsell = 0
    for i in range(len(lists)):
        minus = 0
        plus = 0
        if i > day:
            for j in range(day):
                a = int(lists[i-j-1][1])-int(lists[i-j][1])
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
                coin += buycoin/int(lists[i][1])
                countbuy += 1
            if rsi > 70:
                buyjpy = coin*val
                jpy += buyjpy*int(lists[i][1])
                coin -= buyjpy
                countsell += 1
        result[i][0] = lists[i][0]
        result[i][1] = jpy
        result[i][2] = coin
    end = int(jpy+coin*(lists[len(lists)-1][1]))
    bai = end/sjpy
    if login_ok:
        record = Records(name=name, indicator='RSI', first_money=sjpy,
                         from_date=lists[0][0], to_date=lists[-1][0], result=end, times=bai)
        record.save()
    context = {'result': result, 'resultend': end, 'bai': bai, 'resultjpy': jpy,
               'resultcoin': coin, 'countbuy': countbuy, 'countsell': countsell, 'login_ok': login_ok, "name": name}
    return render(request, "mytrade/result.html", context)


def fib(request):
    day = int(request.GET['day'])
    val = int(request.GET['val'])/100
    sjpy = int(request.GET['sjpy'])
    login_ok = request.GET.get('login_ok')
    name = request.GET.get('name')
    jpy = sjpy
    lists = data_get(request)
    coin, buyjpy, buycoin, countbuy, countsell, rsi, trand = 0, 0, 0, 0, 0, 0, 0
    minus, plus = 0, 0
    result = [["", 0, 0]for i in range(len(lists))]
    high, low = [], []
    for i in range(len(lists)):
        minus = 0
        plus = 0
        high, low = [], []
        if i > day:
            for j in range(day):
                a = lists[i-j-1][1]-lists[i-j][1]
                if a < 0:
                    minus -= a
                else:
                    plus += a
            minus /= day
            plus /= day
            rsi = plus/(plus+minus)*100

            for j in range(day):
                high.append(lists[i-j][2])
                if lists[i-j][3] != 0:
                    low.append(lists[i-j][3])
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
                jpy += buyjpy*lists[i][1]
                countsell += 1
            elif rsi < 30:
                buycoin = jpy*val
                jpy -= buycoin
                coin += buycoin/lists[i][1]
                countbuy += 1
            elif rsi > 50:
                if lists[i][3] < min and lists[i][3] != 0:
                    buycoin = jpy*val
                    jpy -= buycoin
                    coin += buycoin/min
                    countbuy += 1
                if lists[i][2] > mid:
                    buyjpy = coin*val
                    coin -= buyjpy
                    jpy += buyjpy*mid
                    countsell += 1

            else:
                if lists[i][3] < mid and lists[i][3] != 0:
                    buycoin = jpy*val
                    jpy -= buycoin
                    coin += buycoin/mid
                    countbuy += 1
                if lists[i][2] > max:
                    buyjpy = coin*val
                    coin -= buyjpy
                    jpy += buyjpy*max
                    countsell += 1

        result[i][0] = lists[i][0]
        result[i][1] = jpy
        result[i][2] = coin
    end = int(coin*lists[len(lists)-1][1]+jpy)
    bai = end/sjpy
    jpy = int(jpy)
    if login_ok:
        record = Records(name=name, indicator='Fibonacci_Retracement', first_money=sjpy,
                         from_date=lists[0][0], to_date=lists[-1][0], result=end, times=bai)
        record.save()
    context = {'resultjpy': jpy, 'resultcoin': coin, 'countbuy': countbuy,
               'countsell': countsell, 'result': result, 'bai': bai, 'resultend': end, "login_ok": login_ok, "name": name}
    return render(request, "mytrade/result.html", context)


def st(request):
    day = int(request.GET['day'])
    val = int(request.GET['val'])/100
    sjpy = int(request.GET['sjpy'])
    login_ok = request.GET.get('login_ok')
    name = request.GET.get('name')
    jpy = sjpy
    lists = data_get(request)
    result = [["", 0, 0]for i in range(len(lists))]
    h = 0
    l = 1000000000000000
    k, d, b, e = 0, 0, 0, 0
    bf, sf = 0, 0
    coin = 0
    cb, cs = 0, 0
    for i in range(len(lists)):
        h = 0
        l = 1000000000000000
        b, e = 0, 0
        if i > day+3:
            for j in range(day):
                if h < lists[i-j][2]:
                    h = lists[i-j][2]
                if l > lists[i-j][3]:
                    l = lists[i-j][3]
            k = (lists[i-1][4]-l)/(h-l)*100
            for j in range(3):
                h = 0
                l = 1000000000000000
                for m in range(day):
                    if h < lists[i-m-j][2]:
                        h = lists[i-m][2]
                    if l > lists[i-m-j][3] and lists[i-m-j][3] != 0:
                        l = lists[i-j-m][3]
                b += h-l
                e += lists[i-j-1][4]-l
            d = e/b*100
            if k < 20 and d < 20 and k < d:
                bf = 1
            elif k > 80 and d > 80 and k > d:
                sf = 1
            elif k < 20 and d < 20 and k > d and bf == 1:
                coin += (jpy*val)/lists[i][1]
                jpy -= jpy*val
                bf = 0
                cb += 1
            elif k > 80 and d > 80 and k < d and sf == 1:
                jpy += coin*val*lists[i][1]
                coin -= coin*val
                sf = 0
                cs += 1
            else:
                bf = 0
                sf = 0
        result[i][0] = lists[i][0]
        result[i][1] = jpy
        result[i][2] = coin
    jpy = int(jpy)
    resultjpy = int(coin*lists[len(lists)-1][1])+jpy
    bai = resultjpy/sjpy
    if login_ok:
        record = Records(name=name, indicator='Stochastic_Oscillator', first_money=sjpy,
                         from_date=lists[0][0], to_date=lists[-1][0], result=resultjpy, times=bai)
        record.save()
    context = {'resultjpy': jpy, 'resultcoin': coin, 'resultend': resultjpy,
               'bai': bai, 'countbuy': cb, 'countsell': cs, 'result': result, "login_ok": login_ok, "name": name}
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


def inquiry(request):
    name = request.GET['name']
    email = request.GET['email']
    inq = request.GET['message']
    subject = 'thank you for your inquiry'
    message = name+'様'+render_to_string('inquiry/message.txt')
    from_email = 'for.send.mail.use.iwa@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    subject = '問い合わせあり'
    recipient_list = ['freelance0918@gmail.com']
    send_mail(subject, email+inq, from_email, recipient_list)
    context = {'SmaForm': SmaForm, 'BreForm': BreForm}
    return render(request, 'mytrade/index.html', context)


def pre_inquiry(request):
    context = {'Inquiry': Inquiry}
    return render(request, 'mytrade/inquiry.html', context)


def pre_register(request):
    context = {'register': Register}
    return render(request, 'mytrade/register.html', context)


def register(request):
    name = request.GET['name']
    password = request.GET['password']
    adress = request.GET['adress']
    tell = request.GET['tell']
    register_date = datetime.datetime.now()
    regist = Users(name=name, password=password, adress=adress, tell=tell,
                   register_date=register_date, last_in_date='2022-09-04')
    regist.save()
    context = {'SmaForm': SmaForm, 'BreForm': BreForm}
    return render(request, 'mytrade/index.html', context)


def pre_login(request):
    context = {'Login': Login}
    return render(request, 'mytrade/login.html', context)


def login(request):
    name = request.GET['name']
    password = request.GET['password']
    login_ok = Users.objects.filter(name=name, password=password).values()
    records = Records.objects.filter(
        name=login_ok[0]['name']).values().order_by('times').reverse()

    if login_ok:
        best = records[0]
        context = {'name': login_ok[0]['name'],
                   'records': records, 'best': best}
        return render(request, 'mytrade/my_page.html', context)
    else:
        context = {'SmaForm': SmaForm, 'BreForm': BreForm}
        return render(request, 'mytrade/index.html', context)


def mypage(request):
    name = request.GET.get('name')
    records = Records.objects.filter(name=name).values().order_by('times')
    best = records[0]
    context = {'name': name, 'records': records, 'best': best}
    return render(request, 'mytrade/my_page.html', context)
