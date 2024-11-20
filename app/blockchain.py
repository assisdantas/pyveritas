from .block import Block
import datetime
import requests
import random

class Blockchain:
    def __init__(self):
        self.chain = [self.CreateGenesisBlock()]
        self.pending_transactions = []
        self.stakes = {}
        self.penalties = {}

    def CreateGenesisBlock(self):
        genesis_transaction = [{"sender":"System", "receiver":"Miner", "amount":50}]
        return Block(0, "0", datetime.datetime.now(datetime.timezone.utc), genesis_transaction)

    def AddStake(self, node_id, stake):
        self.stakes[node_id] = stake

    def SelectValidator(self):
        total_stake = sum(self.stakes.values())
        if total_stake == 0:
            raise ValueError("No nodes have stakes.")
        pick = random.uniform(0, total_stake)
        current = 0
        for node_id, stake in self.stakes.items():
            current += stake
            if current > pick:
                return node_id

    def AddBlock(self, transactions, difficulty=2):
        previous_block = self.chain[-1]
        new_block = Block(
            index=previous_block.index + 1,
            previous_hash=previous_block.hash,
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            transactions=transactions,
            difficulty=difficulty
        )
        self.chain.append(new_block)
        return new_block
    
    def NotifyNodes(new_block):
        nodes = GetAllConnectedNodes()
        for node in nodes:
            try:
                response = requests.post(f'{node}/receive_block', json=new_block.ToDict())
                if response.status_code != 200:
                    print(f"Node {node} failed to accept block")
            except Exception as e:
                print(f"Error notifying node {node}: {e}")

    def PenalizeNode(self, node_id, penalty_amount):
        if node_id in self.stakes:
            self.stakes[node_id] -= penalty_amount
            if self.stakes[node_id] < 0:
                self.stakes[node_id] = 0
            self.penalties[node_id] = self.penalties.get(node_id, 0) + penalty_amount

    def ValidateBlock(self, block):
        previous_block = self.GetLastBlock()
        if block.previous_hash != previous_block.hash:
            return False
        if not self.VerifyProofOfWork(block):
            return False
        return True
    
    def ValidateBlockDistributed(self, block, validators):
        votes = []
        for validator in validators:
            if self.ValidateBlock(block):
                votes.append(True)
            else:
                votes.append(False)
        
        return votes.count(True) > votes.count(False)
