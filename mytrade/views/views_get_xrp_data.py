import requests
import json


def get_xrp(request):
    endPoint = 'https://api.coin.z.com/public'

    path = '/v1/klines?symbol=XRP&interval=1day&date=2022'
    response = requests.get(endPoint + path)

    print(json.dumps(response.json(), indent=2))
    return response


def get_ETH(request):
    endPoint = 'https://api.coin.z.com/public'

    path = '/v1/klines?symbol=ETH&interval=1day&date=2022'
    response = requests.get(endPoint + path)

    print(json.dumps(response.json(), indent=2))
    return response


def get_BTC(request):
    endPoint = 'https://api.coin.z.com/public'

    path = '/v1/klines?symbol=BTC&interval=1day&date=2022'
    response = requests.get(endPoint + path)

    print(json.dumps(response.json(), indent=2))
    return response
