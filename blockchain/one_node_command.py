from hashlib import sha256
import pandas as pd
import requests
import json
import random


# 블록 조회
# requests의 get 방식으로 블록을 조회할 수 잇는 URL API에 운영중인 노드의 모든 블록 데이터를 조회한다.
headers = {'Content-Type' : 'application/json; charset=utf-8'}
res = requests.get("http://localhost:5000/chain", headers=headers)
json.loads(res.content)


# transaction1
# requests의 post 방식을 통하여 거래를 추가할 수 있는 API URL에 거래 내역 데이터를 보낸다.
# test_from 지갑에서 test_to 지갑으로 3개 보냈다.
headers = {'Content-Type' : 'application/json; charset=utf-8'}
data = {
    "sender" : "test_from",
    "recipient" : "test_to",
    "amount" : 3
}
requests.post(
    "http://localhost:5000/transactions/new",
    headers=headers,
    data=json.dumps(data)).content


# 채굴 명령
# requests의 get 방식으로 채굴 실시를 명령하는 URL API에 채굴 시작 신호를 준다.
headers = {'Content-Type' : 'application/json; charset=utf-8'}
res = requests.get("http://localhost:5000/mine")
print(res)
print(res.text)


# transaction2 
headers = {'Content-Type' : 'application/json; charset=utf-8'}
data = {
    "sender" : "test_from",
    "recipient" : "test_to2",
    "amount" : 30
}
requests.post(
    "http://localhost:5000/transactions/new",
    headers=headers,
    data=json.dumps(data)).content


# transaction3
headers = {'Content-Type' : 'application/json; charset=utf-8'}
data = {
    "sender" : "test_from",
    "recipient" : "test_to3",
    "amount" : 300
}
requests.post(
    "http://localhost:5000/transactions/new",
    headers=headers,
    data=json.dumps(data)).content
