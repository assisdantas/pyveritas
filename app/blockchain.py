from .block import Block
import datetime

class Blockchain:
    def __init__(self):
        self.chain = [self.CreateGenesisBlock()]

    def CreateGenesisBlock(self):
        genesis_transaction = [{"sender":"System", "receiver":"Miner", "amount":50}]
        return Block(0, "0", datetime.datetime.now(datetime.timezone.utc), genesis_transaction)
    
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