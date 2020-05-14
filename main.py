from matplotlib import pyplot as plt
from gpss import *


def output_table(table: Table):
    plt.bar(list(table.table.keys()), list(table.table.values()))
    plt.show()


gpss = Gpss(350)
store = Storage(4)
queue = Queue()

s_tbl = Table(lambda t: store.count, 0, 1, 30)
q_tbl = Table(lambda t: queue.count, 0, 1, 30)

gpss.run(
    [Generate(Uniform(0, 86)),
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

