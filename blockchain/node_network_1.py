from hashlib import sha256
from urllib.parse import urlparse
from flask import Flask, request, jsonify
from time import time
import json
import random
import requests


def register_node(self, address):
    parsed_url = urlparse(address)
    self.nodes.add(parsed_url.netloc)


def resolve_conflicts(self):
    # 구동되는 노드들을 저장
    neighbours = self.nodes
    new_block = None
    # 내 블록의 길이 저장
    max_length = len(self.chain)
    for node in neighbours:
        # url을 받아서 requset 통해 체인 정보 저장
        node_url = "http://" + str(node.replace("0.0.0.0", "localhost")) + '/chain'
        response = requsets.get(node_url)
        
        # 웹페이지와 정상적으로 교류가 되면 그 정보 저장
        if response.status_code == 200:
            length = response.json()['length']
            chain = response.json()['chain']
            
            if length > max_length and self.valid_chain(chain):
                max_length = length
                new_block = chain
            else:
                1 == 1
        
        if new_block != None:
            self.chain = new_block
            return True
        
        return False
    
