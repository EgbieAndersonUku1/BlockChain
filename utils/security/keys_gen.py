from Cryptodome.PublicKey import RSA
from Cryptodome import Random


class KeysGen(object):

    @staticmethod
    def gen_private_and_public_keys(bits=1024):
        """"""

        private_key = RSA.generate(bits=bits, randfunc=Random.new().read)
        public_key = private_key.publickey()
        return private_key, public_key