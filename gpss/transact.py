class TransactCounterSingleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TransactCounterSingleton, cls).__new__(cls)
            cls.instance.count = 0
        return cls.instance

    @staticmethod
    def get_id():
        result = TransactCounterSingleton().count
        TransactCounterSingleton().count += 1
        return result


class Transact:
    def __init__(self, move_moment, current_block):
        self.move_moment = move_moment
        self._id = TransactCounterSingleton.get_id()
        self.current_block = current_block
        self.blocked = False

    @property
    def id(self):
        return self._id

    def __str__(self):
        return "{},{},{},{}".format(self.id, round(self.move_moment, 1), type(self.current_block).__name__[:3],
                                    type(self.current_block.next).__name__[:3])
