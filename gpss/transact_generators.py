import random
from .transact import Transact


class TransactGenerator:
    def __init__(self):
        self.generate_moment = 0
        self.block = None

    def get_next(self):
        raise NotImplemented('TransactGenerator is a base class. Use implementations instead')


class Uniform(TransactGenerator):
    def __init__(self, a, b):
        super(Uniform, self).__init__()
        self._a = a
        self._b = b
        self.generate_moment = self._uniform()

    def get_next(self):
        t = self._uniform()
        transact = Transact(self.generate_moment, self.block)
        self.generate_moment += t
        return transact

    def _uniform(self):
        return random.uniform(self._a, self._b)


class Exponential(TransactGenerator):
    def __init__(self, a, lmbd):
        super(Exponential, self).__init__()
        self._lmbd = lmbd
        self._a = a
        self.generate_moment = self._exponential()

    def get_next(self):
        t = self._exponential()
        transact = Transact(self.generate_moment, self.block)
        self.generate_moment += t
        return transact

    def _exponential(self):
        return random.expovariate(1/self._lmbd) + self._a
