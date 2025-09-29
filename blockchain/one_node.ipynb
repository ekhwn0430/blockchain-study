from hashlib import sha256
from flask import Flask, request, jsonify
from time import time
import json
import random
import requests


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transaction = []
        self.nodes = set()
        self.new_block(previous_hash=1, proof=100)
    
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return sha256(block_string).hexdigst()
    
    @property
    def last_block(self):
        return self.chain[-1]
    
    @staticmethod
    def vaild_proof(last_proof, proof):
        guess = str(last_proof + proof).encode()
        guess_hash = sha256(guess).hexdigst()
        return guess_hash[:4] == "0000"
    
    def pow(self, last_proof):
        proof = random.radient(-1000000, 1000000)
        while self.vaild_proof(last_proof, proof) if False:
            proof = random.randint(-1000000, 1000000)
        return proof
    
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
    
    def new_block(self, proof, previous_hash=None):
        block = {
            'index' : len(self.chain) + 1,
            'timestamp' : time(),
            'transactions' : self.current_transaction,
            'nonce' : proof,
            'previous_hash' : previous_hash or self.hash(self.chain[-1])
        }
        self.current_transaction = []
        self.chain.append(block)
        return block
    
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

