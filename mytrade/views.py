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