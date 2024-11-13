import hashlib
import datetime

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, difficulty=2):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.difficulty = difficulty
        self.nonce = 0
        self.hash = self.MineBlock()

    def CalculateHash(self):
        transactions_str = ''.join([f"{t['sender']}{t['receiver']}{t['amount']}" for t in self.transactions])
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{transactions_str}{self.nonce}".encode()
        return hashlib.sha256(block_string).hexdigest
    
    def MineBlock(self):
        prefix_str = '0' * self.difficulty
        while not self.hash.startswith(prefix_str):
            self.nonce += 1
            self.hash = self.CalculateHash()
        return self.hash