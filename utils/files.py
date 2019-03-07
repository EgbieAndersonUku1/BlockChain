
class FileHandler(object):

    file_name = "block_chain.txt"

    @classmethod
    def load(cls):

        with open(cls.file_name, mode="r") as f:
            return f.readlines()

    @classmethod
    def write(cls, data, mode="a"):
        """"""

        with open(cls.file_name, mode=mode) as f:
            f.write(data)

    @classmethod
    def clear_file_content(cls):
        f = open(cls.file_name, mode="w")
        f.close()
