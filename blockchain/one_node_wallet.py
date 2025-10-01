from flask import Flask, url_for, render_template
from flask import request, redirect
from datetime import datetime
import pandas as pd
import requests
import json
import os


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("Login 버튼을 누름")
        input_value = request.form.to_dict(flat=False) ['wallet_id'][0]
        print("Login 지갑주소 : ", input_value)
        
        # 기존 user 정보 확인
        headers = {'Content-Type' : 'application/json; charset=utf-8'}
        res = requests.get("http://localhost:5000/chain", headers=headers)
        status_json = json.loads(res.text)
        status_json['chain']
        tx_amount_l = []
        tx_sender_l = []
        tx_reciv_l = []
        tx_time_l = []
        
        
        # 거래 내역 정리 (df_tx)
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
        
        
        # pyBTC 잔고 현황 정리 (df_status)
        df_sended = pd.DataFrame(df_tx.groupby('sender')['amount'].sum()).reset_index()
        df_sended.columns = ['user', 'sended_amount']
        df_received = pd.DataFrame(df_tx.groupby('recipient')['amount'].sum()).reset_index()
        df_received.columns = ['user', 'received_amount']
        df_status = pd.merge(df_received, df_sended, on='user', how='outer').fillna(0)
        df_status['balance'] = df_status['received_amount'] - df_status['sended_amount']
        df_status
        
        
        # 결과값 랜더링
        if (df_status['user'] == input_value['wallet_id'][0]).sum() == 1:
            print("로그인 성공")
            return  render_template(
                "wallet.html",
                wallet_id = input_value['wallet_id'][0],
                status[df_status['user'] == df_status['user'].iloc[0]['balance'].iloc[0]]
                )
        else:
            return "잘못된 지갑주소입니다."
    
    return render_template('login.html')

