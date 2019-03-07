import json
from collections import OrderedDict

import binascii


class Converter(object):

    @staticmethod
    def to_string(value):
        """"""
        return json.dumps(value, sort_keys=True).encode()

    @staticmethod
    def to_json(value):
        return json.dumps(value)

    @staticmethod
    def de_serialize_file_object(value):
        return json.loads(value)

    @staticmethod
    def to_ordered_dict(list_of_tuples):
        return OrderedDict(list_of_tuples)

    @staticmethod
    def binary_to_string(bytes):
        return binascii.hexlify(bytes).decode('ascii')

    @staticmethod
    def string_to_binary(string):
        return binascii.unhexlify(string)
