import random
from .struct import *
from .transact_generators import TransactGenerator


class Block:
    def __init__(self):
        self.next = None

    def get_generator(self):
        return None

    def receive_transact(self, transact):
        pass

    def can_receive(self, transact):
        return True

    def get_block_interval(self):
        return None


class Generate(Block):
    def __init__(self, transact_generator: TransactGenerator):
        super(Generate, self).__init__()
        self._transact_generator = transact_generator
        transact_generator.block = self

    def get_generator(self):
        return self._transact_generator


class Advance(Block):
    def __init__(self, a, b=None):
        super(Advance, self).__init__()
        self._a = a
        if not b:
            b = a
        self._b = b

    def receive_transact(self, transact):
        transact.move_moment += random.uniform(self._a, self._b)


class Seize(Block):
    def __init__(self, device: Device):
        super(Seize, self).__init__()
        self._device = device

    def can_receive(self, transact):
        return not self._device.seized

    def receive_transact(self, transact):
        self._device.seized = True


class Release(Block):
    def __init__(self, device):
        super(Release, self).__init__()
        self._device = device

    def receive_transact(self, transact):
        self._device.seized = False


class Enter(Block):
    def __init__(self, storage: Storage):
        super(Enter, self).__init__()
        self._storage = storage

    def can_receive(self, transact):
        return self._storage.count < self._storage.capacity

    def receive_transact(self, transact):
        self._storage.count += 1


class Leave(Block):
    def __init__(self, storage: Storage):
        super(Leave, self).__init__()
        self._storage = storage

    def receive_transact(self, transact):
        if self._storage.count == 0:
            raise Exception("Trying leave empty storage!")
        self._storage.count -= 1


class Tabulate(Block):
    def __init__(self, table: Table, value: int = 1):
        super(Tabulate, self).__init__()
        self._table = table
        self._value = value

    def receive_transact(self, transact):
        self._table.tabulate(transact, self._value)


class Enqueue(Block):
    def __init__(self, queue: Queue):
        super(Enqueue, self).__init__()
        self._queue = queue

    def receive_transact(self, transact):
        self._queue.count += 1


class Depart(Block):
    def __init__(self, queue: Queue):
        super(Depart, self).__init__()
        self._queue = queue

    def receive_transact(self, transact):
        self._queue.count -= 1
