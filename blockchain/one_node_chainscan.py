from flask import Flask
from flask import render_template
import pandas as pd
import requests
import json
import os


app = Flask(__name__, template_folder = od.getcwd())

@app.route('/')
def index():
    headers = {'Content-Type' : 'application/json; charset=utf-8'}
    res = requests.get("http://localhost:5000/chain", headers = headers)

    status_json = json.loads(res.text)
    df_scan = pd.DataFrame(status_json['chain'])
    return render_template('/one_node_scan.html', df_scan = df_scan, block_len = len(df_scan))

app.run(port=8080)
