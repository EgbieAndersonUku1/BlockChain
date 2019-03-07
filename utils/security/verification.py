from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from blocks.block import Block
from utils.converter import Converter
from utils.security.hasher import HashImplementer


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
        guess = (str([transaction.to_json() for transaction in transaction]) + str(last_hash) + str(proof)).encode()
        hash_guess = HashImplementer.hash_string_using_sha256(guess)
        return hash_guess[:2] == "00"

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance, check_funds=True):
        """"""

        return all([cls.verify_transaction(trans, get_balance, check_funds=False) for trans in open_transactions])


    @classmethod
    def verify_transaction(cls, transaction, get_balance, check_funds=True):
        """"""
        if check_funds:
            return get_balance() >= transaction.amount
        return None


class TransactionSignatureVerifier(object):

    def __init__(self, transaction):

        self.transaction = transaction

    def verify_transaction_signature(self):

        public_key = self._get_public_key(self.transaction)
        verifier = PKCS1_v1_5.new(public_key)
        pay_load_hash = self._create_payload_hash(self.transaction)

        return verifier.verify(pay_load_hash, Converter.string_to_binary(self.transaction.signature))

    def _get_public_key(self, transaction):
        return RSA.importKey(Converter.string_to_binary(transaction.sender))

    def _create_payload_hash(self, transaction):
        data = ("{}{}{}".format(transaction.sender, transaction.recipient, transaction.amount).encode("utf8"))
        return SHA256.new(data)


