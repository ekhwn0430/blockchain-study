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


# 노드 기본 정보 설정
# 운영할 노드의 ip 주소와 포트 주소를 선언한다.
# 노드의 key 값(node_identifier, 노드 ip + 포트 번호)을 생성하고
# 노드의 채굴 결과 발생하는 수익을 보낼 지갑의 주소(mine_owner)와 채굴 보상값(mine_profit)을 선언한다.
blockchain = Blockchain()
my_ip = 'localhost'
my_port = '5000'
node_identifier = 'node_' + my_port
mine_owner = 'master'
mine_profit = 0.1


# 블록 정보 호출
# 임의의 사용자가 블록체인 정보 호출 시 블록체인 내의 블록의 길이와 블록의 모든 정보를 json 양식으로 리턴한다.
@app.route('/chain', methods=['GET'])
def full_chain():
    print("chain info requested")
    response = {
        'chain' : blockchain.chain, 
        'length' : len(blockchain.chain)
    }
    return jsonify(response), 200


# 신규 거래 추가
# 거래가 발생할 경우 해당 거래 내역은 json 형식으로 요청되며
# 요청 사항 내 거래 내역의 3가지 요소(발신자, 수신자, 보내는 금액)가 있는지 확인하고 없을 경우 400 에러를 배출한다.
# 에러가 없을 경우에는 블록체인 객체의 new_transaction 함수를 활용하여 블록 거래 내에 신규 거래 내역을 추가한다.
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    print("transactions_new! : ", values)
    required = ['sender', 'recipient', 'amount']
    
    if not all(k in values for k in required):
        return 'missing values', 400
    
    index = blockchain.new_transaction(
        values['sender'],
        values['recipient'],
        values['amount']
    )
    response = {'message' : 'Transactions will be added to Block {%s}' % index}

    # 노드 연결을 위해 추가되는 부분
    # 본 노드에 받은 거래 내역 정보를 다른 노드들에 다같이 업데이트해 준다.
    # 신규로 추가된 경우 type이라는 정보가 없다. 해당 내용은 전파가 필요하다.
    if "type" not in values:
        for node in blockchain.nodes:
            headers {'Content-Type' : 'application/json; charset = utf-8'}
            data = {
                'sender' : values['sender'],
                'recipient' : values['recipient'],
                'amount' : values['amount'],
                'type' : 'sharing'   # 전파이기에 sharing이라는 type이 꼭 필요함
            }
            requsets.post(
                "http://" + node + "/transactions/new",
                headers=headers,
                data=json.dumps(data)
                )
            print("share transaction to >>   ", "http://" + node)
    
    return jsonify(response), 201


# 채굴
# 채굴이 시작되면 마지막 블록 내의 nonce 값을 블록 객체의 pow에 넣은 뒤 작업을 시작한다.
# 작업이 완료되고 작업 증명을 위한 nonce 값이 생성되면 mine_owner로부터 노드 운영자에게 채굴 보상이 주어지고
# 최종적으로 전 블록의 해시값을 포함하여 블록 객체의 new_block 함수로 블록이 생성된다.
@app.route('/mine', methods=['GET'])
def mine():
    print("MINING STARTED")
    last_block = blockchain.last_block
    last_proof = last_block['nonce']
    proof = blockchain.pow(last_proof)
    
    blockchain.new_transaction(
        sender = mine_owner,
        recipient = node_identifier,
        amount = mine_profit   # coinbase transaction
    )
    
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    print("MINING FINISHED")
    
    response = {
        'message' : 'new block found',
        'index' : block['index'],
        'transactions' : block['transactions'],
        'nonce' : block['nonce'],
        'previous_hash' : block['previous_hash']
    }
    
    return jsonify(response), 200


# 노드 운영 시작
app = Flask(__name__)
if __name__ == '__main__':
    app.run(host=my_ip, port=my_port)

