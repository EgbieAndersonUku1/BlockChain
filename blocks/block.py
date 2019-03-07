from time import time

from transactions.transaction import Transaction
from utils.converter import Converter
from utils.show import Display
from utils.security.hasher import HashImplementer


class Block(Display):

    def __init__(self, index, previous_hash, transactions, proof, time=time()):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time
        self.transactions = transactions
        self.proof = proof

    @classmethod
    def create_new_block(cls, block_chain, hashed_block_string, transactions, proof):
        return cls(len(block_chain), hashed_block_string, transactions, proof)

    @staticmethod
    def hash_block(block):
        """"""
        hashed_block = block.to_json()
        hashed_block['transactions'] = Transaction.convert_all_transaction_block_to_ordered_dict(hashed_block['transactions'])
        return HashImplementer.hash_string_using_sha256(Converter.to_string(hashed_block))

    def to_json(self):
        return self.__dict__.copy()
