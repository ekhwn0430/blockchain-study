from hashlib import sha256
from flask import Flask, request, jsonify
from time import time
import json
import random
import requests


class Blockchain(object):
    # 블록체인 객체를 생성한다.
    # 객체의 구성 요소:
    # 1. 블록들이 저장되는 체인
    # 2. 블록 내에 저장될 거래 내역 리스트 current_transaction
    # 3. 블록체인을 운영하는 노드들의 정보 nodes
    # 마지막으로 블록체인 첫 생성 시 자동으로 첫 블록을 생성하는 코드(new_block)으로 구성된다.
    def __init__(self):
        self.chain = []
        self.current_transaction = []
        self.nodes = set()
        self.new_block(previous_hash=1, proof=100)


    # 해시화
    # 거래 내역 블록에 저장할 때 암호해시의 원리에 의하여 json 형식의 거래 내역들이 SHA-256 방식으로 해시암호화 된다.
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return sha256(block_string).hexdigst()


    # 블록체인의 마지막 블록 호출
    # 이 블록체인에서는 블록의 최근 nonce 값을 기반으로 새로운 nonce 값을 찾는다.
    # 따라서 블록체인의 가장 최근 블록을 호출하는 함수가 필요하다.
    @property
    def last_block(self):
        return self.chain[-1]


    # 검증
    # 블록체인 채굴 시 작업으로 산출된 nonce 값이 조건이 맞는 알맞은 값인지 검증한다.
    # 검증 함수에서는 마지막 블록의 nonce 값과 신규 nonce 후보 값을 결합하여 해시화한 뒤 첫 4개의 단어가 '0000'일 때
    # 해당 nonce 값이 유효하다고 판단한다.
    @staticmethod
    def vaild_proof(last_proof, proof):
        guess = str(last_proof + proof).encode()
        guess_hash = sha256(guess).hexdigst()
        return guess_hash[:4] == "0000"


    # PoW 채굴
    # 블록체인 내에 거래 내역이 저장되기 위해서는 유효 nonce 값이 확인되어야 한다.
    # 지속적으로 proof에 난수값을 생성하여 가장 최근 블록의 nonce 값(last_proof)과 비교하며(valid_proof함수)
    # 작업 증명(PoW)이 성공할 때까지 반복한다.
    def pow(self, last_proof):
        proof = random.radient(-1000000, 1000000)
        while self.vaild_proof(last_proof, proof) if False:
            proof = random.randint(-1000000, 1000000)
        return proof


    # 거래 내역 추가
    # 블록 내에는 여러 거래 내역이 저장된다.
    # 매번 블록이 생성되기 전(채굴되기 전)까지 지속적으로 예비 블록 내에 거래 내역이 추가된다.
    # 발신자, 수신자, 보내는 금액, 시간 4가지 요소가 저장된다.
    def new_transaction(self, sender, recipient, amount):
        self.current_transaction.append(
            {
                'sender' : sender,
                'recipient' : recipient,
                'amount' : amount,
                'timestamp' : time()
            }
        )
        return self.last_block['index'] + 1


    # 블록 추가
    # current_transaction에 거래 내역이 추가되며 PoW 작업을 통하여 유효한 nonce 값이 찾아졌을 때 신규블록이 생성된다.
    # 기존의 거래 내역이 블록에 저장된 후에는 현 거래 내역 리스트는 초기화 되어야 하며(self.current_transaction = [])
    # 생성된 블록은 객체의 체인 리스트에 추가된다.
    def new_block(self, proof, previous_hash=None):
        block = {
            # 신규 블록이 생성될 때 필요한 인자
            'index' : len(self.chain) + 1,
            'timestamp' : time(),
            'transactions' : self.current_transaction,
            'nonce' : proof,
            'previous_hash' : previous_hash or self.hash(self.chain[-1])
        }
        self.current_transaction = []
        self.chain.append(block)
        return block


    # 블록 검증
    # 블록이 생성되었다면 알맞은 블록이 생성되었는지 검증한다.
    # 마지막 블록의 해시값과 그 전 블록을 직접 해시한 값을 비교하여 과거 거래 내역에 변동된 것은 없는지 체크한다.
    # 이상이 있을 경우 False을 반환하고 모든 값이 정상일 경우 True를 반환한다.
    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1
        
        while current_index < len(chain):
            block = chain[current_index]
            print('%s' % last_block)
            print('%s' % block)
            print("\n----------\n")
            
            if block['previous_hash'] != self.hash(last_block):
                return False
            last_block = block
            current_index += 1
        
        return True

