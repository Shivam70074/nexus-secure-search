import hashlib
import time
import json
from typing import List, Dict, Any

class Block:
    def __init__(self, index: int, timestamp: float, transactions: List[Dict[str, Any]], previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.compute_hash()

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.difficulty = 2
        self.create_genesis_block()
        self._backup_chain = []
        self._save_backup()

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), [{"message": "Genesis Block"}], "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def add_block(self, transactions: List[Dict[str, Any]]):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), time.time(), transactions, previous_block.hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self._save_backup()

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.compute_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def simulate_tamper(self, block_index: int, new_data: Any):
        if 0 < block_index < len(self.chain):
            self.chain[block_index].transactions.append(new_data)

    def restore_chain(self):
        self.chain = []
        for b_data in self._backup_chain:
            b = Block(b_data['index'], b_data['timestamp'], b_data['transactions'].copy(), b_data['previous_hash'], b_data['nonce'])
            b.hash = b_data['hash']
            self.chain.append(b)
            
    def _save_backup(self):
        self._backup_chain = [{
            'index': b.index,
            'timestamp': b.timestamp,
            'transactions': b.transactions.copy(),
            'previous_hash': b.previous_hash,
            'nonce': b.nonce,
            'hash': b.hash
        } for b in self.chain]

ledger = Blockchain()
