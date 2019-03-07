
class FileHandler(object):


    @classmethod
    def load(cls, file_name="block_chain.txt"):

        with open(file_name, mode="r") as f:
            return f.readlines()

    @classmethod
    def write(cls, data, mode="a", file_name="block_chain.txt"):
        """"""

        with open(file_name, mode=mode) as f:
            f.write(data)

    @classmethod
    def clear_file_content(cls, file_name="block_chain.txt"):
        f = open(file_name, mode="w")
        f.close()
