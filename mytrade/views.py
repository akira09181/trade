from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import math
from .models import Input
from .forms import SmaForm,BreForm


# Create your views here.
def index(request):
    Bre = BreForm(request.GET)
    Sma = SmaForm(request.GET)
    response = requests.get('http://nipper.work/btc/index.php?market=bitFlyer&coin=BTCJPY&periods=86400&after=1420070400')
    bs = BeautifulSoup(response.text, "html.parser")
    value = bs.find_all("td")
    lists = []
    num = int(len(value)/6)
    for i in range(int(len(value)/6)):
        li = []
        for j in range(6):
            li.append(value[-(i*6+j)-1].get_text())
        lists.append(li)
        c = Input(date=li[5][:10],start=int(li[4]),high=int(li[3]),low=int(li[2]),end=int(li[1]),volume=float(li[0]))
        c.save()
        
    
        
    
    context = {"value":lists,"num":num,"BreForm":BreForm,"SmaForm":SmaForm}
    return render(request,"mytrade/index.html",context)
def sma(request):
    response = requests.get('http://nipper.work/btc/index.php?market=bitFlyer&coin=BTCJPY&periods=86400&after=1420070400')
    bs = BeautifulSoup(response.text, "html.parser")
    value = bs.find_all("td")
    lists = []
    num = int(len(value)/6)
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
    trandflag=0
    avl = 0
    avs = 0
    sellf = 0
    buyf = 0
    sjpy = int(request.GET['sjpy'])
    jpy = sjpy
    bitcoin = 0
    buycoin=0
    buyjpy=0
    result = [["",0,0]for i in range(len(lists))]
    for i in range(len(lists)):
        avl = 0
        avs = 0
        if i >= lo:
            for j in range(lo):
                avl += int(lists[i-j][2])
            avl/=lo
            for j in range(sh):
                avs += int(lists[i-j][2])
            avs/=sh
        if avl < avs and trandflag == 0:
            trandflag=1
            buycoin = jpy*va
            jpy-=buycoin
            bitcoin+= buycoin/int(lists[i][2])
        elif avl > avs and trandflag == 1:
            trandflag = 0
            buyjpy = bitcoin*va
            bitcoin-=bitcoin*va
            jpy += buyjpy * int(lists[i][2])
        result[i][0]=lists[i][0][:10]
        result[i][1]=jpy
        result[i][2]=bitcoin
    resultend = int(bitcoin*int(lists[-1][2])+jpy)
    bai = resultend/sjpy
    jpy = int(jpy)         
    context = {"result":result,"resultjpy":jpy,"resultcoin":bitcoin,"resultend":resultend,"bai":bai}
    return render(request,"mytrade/sma.html",context)
def breverse(request):
    response = requests.get('http://nipper.work/btc/index.php?market=bitFlyer&coin=BTCJPY&periods=86400&after=1420070400')
    bs = BeautifulSoup(response.text, "html.parser")
    value = bs.find_all("td")
    lists = []
    num = int(len(value)/6)
    for i in range(int(len(value)/6)):
        li = []
        for j in range(6):
            
            li.append(value[i*6+j].get_text())
        if li[1]!="0":    
            lists.append(li)
    day = request.GET["day"]
    val = request.GET["val"]
    da = int(day)
    va = int(val)/100
    sjpy = int(request.GET['sjpy'])
    jpy=sjpy
    ave = 0
    dtb = 0
    bitcoin=0
    buycoin=0
    buyjpy=0
    
    result = [["",0,0]for i in range(len(lists))]
    for i in range(len(lists)):
        if i >da:
            for j in range(da):
                ave += int(lists[i-j][1])
            ave/=da
            for j in range(da):
                dtb += (int(lists[i-j][1])-ave)**2
            dtb/=da
            
            dtb=math.sqrt(dtb)
            
            if int(lists[i][1])<ave-dtb*2:
                buycoin = jpy*va
                jpy-=buycoin
                
                bitcoin+= buycoin/int(lists[i][1])
            elif int(lists[i][1])>ave+dtb*2:
                buyjpy = bitcoin*va
                bitcoin-=buyjpy
                jpy+=buyjpy*int(lists[i][1])
        result[i][0]=lists[i][0][:10]
        result[i][1]=jpy
        result[i][2]=bitcoin
    resultend = int(bitcoin*int(lists[-1][1])+jpy)
    bai= resultend/sjpy
    jpy = int(jpy)
    context={"resultend":resultend,"result":result,"resultjpy":jpy,"resultcoin":bitcoin,"bai":bai}
    return render(request,"mytrade/breverse.html",context)
def bbreak(request):
    response = requests.get('http://nipper.work/btc/index.php?market=bitFlyer&coin=BTCJPY&periods=86400&after=1420070400')
    bs = BeautifulSoup(response.text, "html.parser")
    value = bs.find_all("td")
    lists = []
    num = int(len(value)/6)
    for i in range(int(len(value)/6)):
        li = []
        for j in range(6):
            
            li.append(value[i*6+j].get_text())
        if li[1]!="0":    
            lists.append(li)
    day = request.GET["day"]
    val = request.GET["val"]
    da = int(day)
    va = int(val)/100
    sjpy = int(request.GET['sjpy'])
    jpy=sjpy
    ave = 0
    dtb = 0
    bitcoin=0
    buycoin=0
    buyjpy=0
    countbuy=0
    countsell = 0
    
    result = [["",0,0]for i in range(len(lists))]
    for i in range(len(lists)):
        ave = 0
        dtb = 0
        if i > da:
            for j in range(da):
                ave += int(lists[i-j][1])
            ave/=da
            for j in range(da):
                dtb += (int(lists[i-j][1])-ave)**2
            dtb/=da
            
            dtb=math.sqrt(dtb)
            if int(lists[i][1]) > ave+2*dtb:
                buycoin = jpy*va
                jpy-=buycoin
                bitcoin+= buycoin/int(lists[i][1])
                countbuy +=1
                print(i,"0",ave,dtb,lists[i][1])
            elif int(lists[i][1]) < ave-2*dtb:
                buyjpy = bitcoin*va
                bitcoin-=buyjpy
                jpy+=buyjpy*int(lists[i][1])
                countsell+=1
        result[i][0]=lists[i][0][:10]
        result[i][1]=jpy
        result[i][2]=bitcoin
    resultend = int(bitcoin*int(lists[-1][1])+jpy)
    bai= resultend/sjpy
    jpy = int(jpy)
    context={"resultend":resultend,"result":result,"resultjpy":jpy,"resultcoin":bitcoin,"bai":bai,
             "countbuy":countbuy,"countsell":countsell }
    return render(request,"mytrade/result.html",context)
def macd(request):
    
    response = requests.get('http://nipper.work/btc/index.php?market=bitFlyer&coin=BTCJPY&periods=86400&after=1420070400')
    bs = BeautifulSoup(response.text, "html.parser")
    value = bs.find_all("td")
    lists = []
    num = int(len(value)/6)
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
    trandflag=0
    avl = 0
    avs = 0
    sellf = 0
    buyf = 0
    sjpy = int(request.GET['sjpy'])
    jpy=sjpy
    bitcoin = 0
    buycoin=0
    buyjpy=0
    result = [["",0,0]for i in range(len(lists))]
    for i in range(len(lists)):
        avl = 0
        avs = 0
        countl = 0
        counts = 0
        if i >= lo:
            for j in range(lo):
                avl += int(lists[i-j][2])*(lo-j)
                countl+=(lo-j)
            avl/=countl
            for j in range(sh):
                avs += int(lists[i-j][2])*(sh-j)
                counts+=(sh-j)
            avs/=counts
        if avl < avs and trandflag == 0:
            trandflag=1
            buycoin = jpy*va
            jpy-=buycoin
            bitcoin+= buycoin/int(lists[i][2])
        if avl > avs and trandflag == 1:
            trandflag = 0
            buyjpy = bitcoin*va
            bitcoin-=bitcoin*va
            jpy += buyjpy * int(lists[i][2])
        result[i][0]=lists[i][0][:10]
        result[i][1]=jpy
        result[i][2]=bitcoin
    resultend = int(bitcoin*int(lists[-1][2])+jpy)
    bai = resultend/sjpy
    jpy = int(jpy)         
    context = {"result":result,"resultjpy":jpy,"resultcoin":bitcoin,"resultend":resultend,"bai":bai}
    return render(request,"mytrade/result.html",context)
def results(request):
    return HttpResponse("This is result")

def rsi(request):
    c = Input.objects.all().values().order_by('date')
    day = int(request.GET['day'])
    val = int(request.GET['val'])/100
    sjpy = int(request.GET['sjpy'])
    jpy=sjpy
    coin=0
    ave = 0
    plus=0
    minus=0
    rsi=0
    buyjpy=0
    buycoin=0
    result=[["",0,0]for i in range(len(c))]
    countbuy=0
    countsell=0
    for i in range(len(c)):
        minus=0
        plus=0
        if i >day:
            for j in range(day):             
                a = int(c[i-j-1]['start'])-int(c[i-j]['start'])
                if a < 0:
                    minus-=a
                else:
                    plus+=a
            minus/=day
            plus/=day
            rsi=plus/(plus+minus)*100
            if rsi < 30:
                buycoin=jpy*val
                jpy-=buycoin
                coin+=buycoin/int(c[i]['start'])
                countbuy+=1
            if rsi > 70:
                buyjpy=coin*val
                jpy+=buyjpy*int(c[i]['start'])
                coin-=buyjpy
                countsell+=1
        result[i][0]=c[i]['date']
        result[i][1]=jpy
        result[i][2]=coin
    end=int(jpy+coin*(c[len(c)-1]['start']))
    bai=end/sjpy
    context={'result':result,'resultend':end,'bai':bai,'resultjpy':jpy,'resultcoin':coin,'countbuy':countbuy,'countsell':countsell}
    return render(request,"mytrade/result.html",context)
def fib(request):
    day = int(request.GET['day'])
    val = int(request.GET['val'])/100
    sjpy = int(request.GET['sjpy'])
    jpy = sjpy
    c = Input.objects.all().values().order_by('date')
    coin,buyjpy,buycoin,countbuy,countsell,rsi,trand=0,0,0,0,0,0,0
    minus,plus=0,0
    result = [["",0,0]for i in range(len(c))]
    high,low=[],[]
    for i in range(len(c)):
        minus=0
        plus=0
        high,low=[],[]
        if i > day:
            for j in range(day):
                a = c[i-j-1]['start']-c[i-j]['start']
                if a < 0:
                    minus-=a
                else:
                    plus+=a
            minus/=day
            plus/=day
            rsi=plus/(plus+minus)*100
            if rsi > 70:
                trand=1
            elif rsi < 30:
                trand=-1
            for j in range(day):
                high.append(c[i-j]['high'])
                if c[i-j]['low']!=0:
                    low.append(c[i-j]['low'])
            high.sort()
            low.sort()
            h=high[-1]
            l=low[0]
            min=(h-l)*0.236+l
            min2=(h-l)*0.382+l
            mid =(h-l)*0.5+l
            max2=(h-l)*0.618+l
            max=(h-l)*0.784+l
            hh=(h-l)*1.618+l
            h2=(h-l)*1.382+l
            hm=(h-l)*1.5+l
            if trand==1:
                if c[i]['low']<mid and c[i]['low']!=0:
                    buycoin=jpy*val
                    
                    jpy-=buycoin
                    coin+=buycoin/c[i]['low']
                    countbuy+=1
                if c[i]['high']>max:
                    buyjpy=coin*val
                    coin-=buyjpy
                    jpy+=buyjpy*c[i]['high']
                    countsell+=1
                    
                    
            elif trand==-1:
                if c[i]['low']<min and c[i]['low']!=0:
                    buycoin=jpy*val
                    jpy-=buycoin
                    coin+=buycoin/c[i]['low']
                    countbuy+=1
                if c[i]['high']>max2:
                    buyjpy=coin*val
                    coin-=buyjpy
                    jpy+=buyjpy*c[i]['high']
                    countsell+=1
                    
        result[i][0]=c[i]['date']
        result[i][1]=jpy
        result[i][2]=coin
    end=int(coin*c[len(c)-1]['start']+jpy)
    bai=end/sjpy
            
    
    context={'resultjpy':jpy,'resultcoin':coin,'countbuy':countbuy,'countsell':countsell,'result':result,'bai':bai}
    return render(request,"mytrade/result.html",context)