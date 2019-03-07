
class Display(object):

    def __repr__(self):
        return str(self.to_json())

    def to_json(self):
        return self.__dict__.copy()