from Crypto.PublicKey import RSA
import Crypto.Random


class KeysGen(object):

    @staticmethod
    def gen_private_and_public_keys(bits=1024):
        """"""

        private_key = RSA.generate(bits=bits, randfunc=Crypto.Random.new().read)
        public_key = private_key.publickey()
        return private_key, public_key