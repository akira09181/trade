from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup



# Create your views here.
def index(request):
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
    
        
    
    context = {"value":lists,"num":num}
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
    jpy = 1000000
    bitcoin = 0
    buycoin=0
    buyjpy=0
    result = [["",0,0]for i in range(len(lists))-lo]
    for i in range(len(lists)-lo):
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
        result[i][0]=lists[i][1][:10]
        result[i][1]=jpy
        result[i][2]=bitcoin
    resultend = bitcoin*int(lists[-1][2])+jpy
    bai = resultend/1000000            
    context = {"result":result,"resultjpy":int(jpy),"resultcoin":bitcoin,"resultend":resultend,"bai":bai}
    return render(request,"mytrade/sma.html",context)
def results(request):
    return HttpResponse("This is result")