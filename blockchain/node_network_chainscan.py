from flask import Flask
from flask import render_template
import pandas as pd
import requests
import json
import os
import random


app = Flask(__name__, template_folder = od.getcwd())

node_port_list = [5000, 5001, 5002]

# 블록 체인 내 블록 정보를 제공하는 url에 request 방식으로 데이터를 요청
# 요청 결과 데이터(res.text)를 json으로 로드
# 결과 데이터를 데이터프레임으로 정리
# front 구성 내용이 담길 one_node_scan.html 파일에 데이터프레임 정보와 블록의 길이 제공
@app.route('/')
def index():
    headers = {'Content-Type' : 'application/json; charset=utf-8'}
    node_id = random.choice(node_port_list)
    res = requests.get("http://localhost:" + 5000 + "/chain", headers = headers)
    
    status_json = json.loads(res.text)
    df_scan = pd.DataFrame(status_json['chain'])
    return render_template('/one_node_scan.html', df_scan = df_scan, block_len = len(df_scan))

app.run(port=8080)
