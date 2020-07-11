import random
from .struct import *
from .transact_generators import TransactGenerator


class Block:
    def __init__(self):
        self._next = None

    def get_generator(self):
        return None

    def receive_transact(self, transact, current_time):
        return transact

    def can_receive(self, transact, current_time):
        return True

    def get_next_block(self, transact):
        return self._next

    def set_next_block(self, next_block):
        self._next = next_block

    def on_leave(self, transact, current_time):
        pass


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

    def receive_transact(self, transact, current_time):
        transact.move_moment += random.uniform(self._a, self._b)
        return transact


class Seize(Block):
    def __init__(self, device: Device):
        super(Seize, self).__init__()
        self._device = device

    def can_receive(self, transact, current_time):
        return not self._device.seized

    def receive_transact(self, transact, current_time):
        self._device.seized = True
        return transact


class Release(Block):
    def __init__(self, device):
        super(Release, self).__init__()
        self._device = device

    def receive_transact(self, transact, current_time):
        self._device.seized = False
        return transact


class Enter(Block):
    def __init__(self, storage: Storage):
        super(Enter, self).__init__()
        self._storage = storage

    def can_receive(self, transact, current_time):
        return self._storage.count < self._storage.capacity

    def receive_transact(self, transact, current_time):
        self._storage.count += 1
        return transact


class Leave(Block):
    def __init__(self, storage: Storage):
        super(Leave, self).__init__()
        self._storage = storage

    def receive_transact(self, transact, current_time):
        if self._storage.count == 0:
            raise Exception("Trying to leave empty storage!")
        self._storage.count -= 1
        return transact


class Tabulate(Block):
    def __init__(self, table: Table, value: int = 1):
        super(Tabulate, self).__init__()
        self._table = table
        self._value = value

    def receive_transact(self, transact, current_time):
        self._table.tabulate(transact, self._value)
        return transact


class Enqueue(Block):
    def __init__(self, queue: Queue):
        super(Enqueue, self).__init__()
        self._queue = queue

    def receive_transact(self, transact, current_time):
        self._queue.enqueue(transact, current_time)
        return transact


class Depart(Block):
    def __init__(self, queue: Queue):
        super(Depart, self).__init__()
        self._queue = queue

    def receive_transact(self, transact, current_time):
        self._queue.dequeue(transact, current_time)
        return transact


class RandomSplitter(Block):
    def __init__(self, blocks):
        super(RandomSplitter, self).__init__()
        self.blocks = list(blocks)

    def get_next_block(self, query):
        return random.choice(self.blocks)

    def set_next_block(self, next_block):
        for block in self.blocks:
            block.set_next_block(next_block)
