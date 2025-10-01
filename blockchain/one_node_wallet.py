from flask import Flask, url_for, render_template
from flask import request, redirect
from datetime import datetime
import pandas as pd
import requests
import json
import os


# Flask app 선언
app = Flask(__name__, template_folder = os.getcwd())


# login 기능 구현
# 로그인 페이지에서 로그인 버튼을 클릭하면 POST 방식을 통하여 백앤드에 접속하게 된다.
# post임을 감지하여 입력된 지갑 아이디가 input_value에 저장된다.
# 블록체인의 블록 정보 조회 URL에 request의 GET 방식으로 접속하여 정보를 받아 오며
# 이후 pandas를 통해 현 계정별 잔액을 조회하고 로그인한 계정이 데이터프레임의 user 값과 동일할 경우
# 해당 계정의 잔고 값과 함께 로그인이 성공된 wallet.html 페이지로 렌더링해준다.
@app.route('/', methods=['GET', 'POST'])
def login():
    # POST 감지
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
        if (df_status['user'] == input_value).sum() == 1:
            print("로그인 성공")
            return  render_template(
                "wallet.html",
                wallet_id = input_value,
                status[df_status['user'] == input_value]['balance'].iloc[0]
                )
        else:
            return "잘못된 지갑주소입니다."
    
    return render_template('login.html')


# 지갑 기능 구현
# 로그인이 성공한 경우 로그인한 사용자의 지갑 ID, 잔고를 리턴해준다.(70 ~ 74)
# 사용자가 보내고자 하는 USER-ID와 보낼 금액을 입력한 뒤 보내기 버튼을 클릭하면 POST 방식으로 백앤드의 wallet에 접속하게 된다.
# POST임을 감지한뒤 송금될 금액, 송금 받을 지갑 아이다, 송금하는 지갑 아이디가 send_value, send_target, send_from에 저장된다.
# 보내는 금액이 정상적일 경우 블록체인의 송금 URL에 request의 POST 방식으로 송금 데이터를 업데이트해준다.
@app.route('/wallet', methods=['GET', 'POST'])
def wallet():
    if request.method == 'POST':
        send_value = int(request.form.to_dict(flat=False)['send_value'][0])
        send_target = request.form.to_dict(flat=False)['send_target'][0]
        send_from = request.form.to_dict(flat=False)['send_from'][0]
        print("Login Wallet ID :", send_from)
    
        if send_value > 0:
            print("Send Amount :", send_value)
            # transaction 입력
            headers = {'Content-Type' : 'application/json; charset=utf-8'}
            data = {
                "sender" : send_from,
                "recipient" : send_target,
                "amount" : send_value
            }
            requests.post(
                "http://localhost:5000/transactions/new",
                headers = headers,
                data = json.dumps(data)
                )
            
            return "전송 완료!"
            
        else:
            return "0 pyBTC 이상 보내주세요"
        
    return render_template('wallet.html')


# 지갑 사이트 실행
app.run(port=8001)
