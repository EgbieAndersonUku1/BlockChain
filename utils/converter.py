import json
from collections import OrderedDict


class Converter(object):

    @staticmethod
    def to_string(value):
        """"""
        return json.dumps(value, sort_keys=True).encode()

    @staticmethod
    def to_json(value):
        return json.dumps(value)

    @staticmethod
    def de_serialize_object(value):
        return json.loads(value)

    @staticmethod
    def to_ordered_dict(list_of_tuples):
        return OrderedDict(list_of_tuples)