from utils.converter import Converter
from utils.files import FileHandler
from utils.security.keys_gen import KeysGen
from utils.security.signer import SignSignature
from utils.security.verification import TransactionSignatureVerifier


class Wallet(object):

    def __init__(self):

        self.private_key = None
        self.public_key = None
        self._file_name = "wallet.txt"

    def create_keys(self):
        """"""
        self.private_key, self.public_key = self._generate_private_and_public_keys()

    def _generate_private_and_public_keys(self):
        """"""
        private_key, public_key = KeysGen.gen_private_and_public_keys()

        private_key_str = Converter.binary_to_string(private_key.exportKey(format="DER"))
        public_key_str = Converter.binary_to_string(public_key.exportKey(format="DER"))

        return private_key_str, public_key_str

    def save_keys(self):
        """"""

        if self.private_key is not None and self.public_key is not None:

            try:
                FileHandler.clear_file_content(self._file_name)
                FileHandler.write(file_name=self._file_name, data=self.public_key)
                FileHandler.write(file_name=self._file_name, data="\n")
                FileHandler.write(file_name=self._file_name, data=self.private_key)
            except (IndexError, IOError):
                print("Failed to save keys")
                return False
            return True

    def load_existing_keys(self):

        try:
            keys = FileHandler.load(self._file_name)
        except (IOError, IndexError):
            return False

        self.public_key, self.private_key = keys[0][:-1], keys[1]
        return True

    def sign_transaction(self, sender, recipient, amount):

        signer = SignSignature(sender, recipient, amount, self.private_key)
        return signer.sign_transaction()

    @staticmethod
    def verify_signature(transaction):

        verify = TransactionSignatureVerifier(transaction)
        return verify.verify_transaction_signature()









