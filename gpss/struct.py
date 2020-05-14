from .transact import Transact


class Device:
    def __init__(self):
        self.seized = False


class Storage:
    def __init__(self, capacity):
        self.capacity = capacity
        self.count = 0


class Table:
    def __init__(self, tabulate_func, start, step, step_count):
        self._tabulate_func = tabulate_func
        self._start = start
        self._step = step
        self._step_count = step_count
        self.table = dict((i, 0) for i in range(self._start, self._step_count*self._step, self._step))

    def tabulate(self, transact, value=1):
        key = self._tabulate_func(transact)
        if key > self._step_count*self._step - self._step:
            key = self._step_count*self._step - self._step
        self.table[key] += value

    def __str__(self):
        return str(self.table)


class QTable(Table):
    def __init__(self, start, step, step_count):
        self.queue = None
        super(QTable, self).__init__(lambda t: 0, start, step, step_count)


class Queue:
    def __init__(self, qtable=None):
        self.count = 0
        self.qtable = qtable

    def enqueue(self, transact):
        self.count += 1

    def dequeue(self, transact):
        self.count -= 1
