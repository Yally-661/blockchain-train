import logging
import sys
import time
import hashlib
import json

import utils

MINING_DIFFICULTY = 3
MINING_SENDER = 'A'
MINING_REWARD = 1

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


class BlockChain(object):
    def __init__(self, blockchain_address=None) -> None:
        self.transaction_pool = []
        self.chain = []
        self.create_block(0, self.hash({}))
        self.blockchain_address = blockchain_address

    def create_block(self, nonce, previous_hash):
        block = {
            'timestamp': time.time(),
            'transactions': self.transaction_pool,
            'nonce': nonce,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        self.transaction_pool = []
        return block

    def hash(self, block):
        sorted_block = json.dumps(block, sort_keys=True)
        return hashlib.sha256(sorted_block.encode()).hexdigest()

    def add_transaction(self, sender_address, recipient_address, value):
        transaction = utils.sorted_dict_by_key({
            'sender_address': sender_address,
            'recipient_address': recipient_address,
            'value': float(value)
        })
        self.transaction_pool.append(transaction)
        return True

    def valid_proof(self, transactions, previous_hash, nonce, difficulty=MINING_DIFFICULTY):
        guess_block = utils.sorted_dict_by_key({
            'transactions': transactions,
            'nonce': nonce,
            'previous_hash': previous_hash
        })
        guess_hash = self.hash(guess_block)
        return guess_hash[:difficulty] == '0' * difficulty

    def proof_of_work(self):
        transactions = self.transaction_pool.copy()
        previous_hash = self.hash(self.chain[-1])
        nonce = 0
        while self.valid_proof(transactions, previous_hash, nonce) is False:
            nonce += 1
        return nonce

    def mining(self):
        self.add_transaction(
            sender_address=MINING_SENDER,
            recipient_address=self.blockchain_address,
            value=MINING_REWARD
        )
        nonce = self.proof_of_work()
        previous_hash = self.hash(self.chain[-1])
        self.create_block(nonce, previous_hash)
        logger.info({'action': 'mining', 'status': 'success'})
        return True

    def calculate_total_amount(self, blockchain_address):
        total_amount = 0.0
        for block in self.chain:
            for transaction in block['transactions']:
                value = float(transaction['value'])
                if blockchain_address == transaction['sender_address']:
                    total_amount -= value
                if blockchain_address == transaction['recipient_address']:
                    total_amount += value
        return total_amount


if __name__ == '__main__':
    adress = 'my_blockchain_address'
    block_chain = BlockChain(adress)
    block_chain.add_transaction('a', 'b', 1)
    block_chain.mining()
    block_chain.add_transaction('c', 'd', 2)
    block_chain.add_transaction('e', 'f', 0.5)
    block_chain.mining()
    utils.pprint(block_chain.chain)

    print('my_total_amount', block_chain.calculate_total_amount(adress))
