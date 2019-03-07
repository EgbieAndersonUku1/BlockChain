import hashlib


class HashImplementer(object):

    @staticmethod
    def hash_string_using_sha256(value):
        """hash_string_using_sha256(str) -> hashed_str"""
        return hashlib.sha256(value).hexdigest()