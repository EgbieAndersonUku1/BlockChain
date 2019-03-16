from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA256

from utils.converter import Converter


class SignSignature(object):

    def __init__(self, sender, recipient, amount, private_key):
        self.sender = str(sender)
        self.recipient = str(recipient)
        self.amount = str(amount)
        self.private_key = private_key
        self._payload = None

    @property
    def payload_hash(self):
        return self._payload

    @payload_hash.setter
    def payload_hash(self, payload):
        self._payload = payload

    def sign_transaction(self):

        signer = PKCS1_v1_5.new(RSA.importKey(Converter.string_to_binary(self.private_key)))

        self._create_payload_hash()

        signature = signer.sign(self.payload_hash)

        return Converter.binary_to_string(signature)

    def _create_payload_hash(self):
        data = ("{}{}{}".format(self.sender, self.recipient, self.amount).encode("utf8"))
        self._payload = SHA256.new(data)




