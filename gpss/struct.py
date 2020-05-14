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
        val = self._tabulate_func(transact)
        key = val
        if key not in self.table:
            key = min(self.table, key=lambda k: abs(k-val))
        self.table[key] += value

    def __str__(self):
        return str(self.table)


class QTable(Table):
    def __init__(self, start, step, step_count):
        super(QTable, self).__init__(None, start, step, step_count)

    def tabulate_q(self, transact, time):
        key = int(time)
        if key not in self.table:
            key = min(self.table, key=lambda k: abs(k - int(time)))
        self.table[key] += 1


class Queue:
    def __init__(self, qtable=None):
        self.count = 0
        self.qtable = qtable
        self.transacts_time = {}

    def enqueue(self, transact: Transact, current_time):
        self.count += 1
        self.transacts_time[transact.id] = current_time

    def dequeue(self, transact: Transact, current_time):
        self.count -= 1
        if self.qtable:
            self.qtable.tabulate_q(transact, current_time-self.transacts_time[transact.id])
        del self.transacts_time[transact.id]

