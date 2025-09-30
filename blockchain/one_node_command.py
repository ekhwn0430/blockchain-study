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


# 거래 내역이 증가함에 따라 json 방식으로 확인이 어렵기 때문에 pandas를 활용하여 거래 내역을 Table로 확인한다.
status_json = json.loads(res.text)
status_json['chain']
tx_amount_l = []
tx_sender_l = []
tx_reciv_l = []
tx_time_l = []

for chain_index in range(len(status_json['chain'])):
    chain_tx = status_json['chain'][chain_index]['transactions']

    for each_tx in range(len(chain_tx)):
        tx_amount_l.append(chain_tx[each_tx]['amount'])
        tx_sender_l.append(chain_tx[each_tx]['sender'])
        tx_reciv_l.append(chain_tx[each_tx]['recipient'])
        tx_time_l.append(chain_tx[each_tx]['timestamp'])

df_tx = pd.DataFrame()
df_tx['timestamp'] = tx_time_l
df_tx['sender'] = tx_sender_l
df_tx['recipient'] = tx_reciv_l
df_tx['amount'] = tx_amount_l

df_tx
