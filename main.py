from matplotlib import pyplot as plt
from gpss import *


def output_table(table: Table):
    plt.bar(list(table.table.keys()), list(table.table.values()), width=0.8*table._step)
    plt.show()


gpss = Gpss(40000)

store = Storage(10)
s_tbl = Table(lambda t: store.count, 0, 1, 30)

qt_tbl = QTable(0, 10, 30)
queue = Queue(qt_tbl)
q_tbl = Table(lambda t: queue.count, 0, 1, 30)

gpss.run(
    [Generate(Exponential(0, 43)),
     Enqueue(queue),
     Enter(store),
     Tabulate(q_tbl),
     Tabulate(s_tbl),
     Depart(queue),
     Advance(179, 259),
     Leave(store)]
)

output_table(s_tbl)
output_table(q_tbl)
output_table(qt_tbl)
