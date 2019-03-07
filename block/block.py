from utils.converter import Converter
from utils.printable import Display
from utils.security.hasher import HashImplementer
from utils.zone import get_timezone


class Block(Display):

    def __init__(self, index, previous_hash, transactions, proof, time_stamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.proof = proof
        self.time_stamp = get_timezone() if time_stamp is None else time_stamp

    @classmethod
    def create_block(cls, hashed_block, block_chain, open_transactions, proof, time_stamp=None):
        """"""
        return cls(len(block_chain), hashed_block, open_transactions, proof, time_stamp)

    @staticmethod
    def hash_block(block):

        hashed_block = block.to_json()
        hashed_block['transactions'] = [tx.to_ordered_dictionary() for tx in hashed_block['transactions']]
        json = Converter.to_json(hashed_block)
        return HashImplementer.hash_string_using_sha256(Converter.to_string(json))