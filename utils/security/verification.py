from utils.security.hasher import HashImplementer
from block.block import Block


class Verification(object):

    @classmethod
    def verify_chain(cls, block_chain):
        """Allows the block chain to be verified"""

        for index, block in enumerate(block_chain):
            if index == 0:
                continue
            elif block.previous_hash != Block.hash_block(block_chain[index - 1]):
                return False
            elif not cls.check_proof_validation(block.transactions[:-1], block.previous_hash, block.proof):
                print("Proof of work invalid")
                return False
        return True

    @classmethod
    def check_proof_validation(cls, transaction, last_hash, proof):
        """"""
        guess = (str([tx.to_json() for tx in transaction]) + str(last_hash) + str(proof)).encode()
        hash_guess = HashImplementer.hash_string_using_sha256(guess)
        return hash_guess[:2] == "00"

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        """"""
        return all([cls.verify_transaction(tx, get_balance) for tx in open_transactions])

    @classmethod
    def verify_transaction(cls, transaction, get_balance):
        """"""
        return get_balance(transaction.sender, None) >= transaction.amount
