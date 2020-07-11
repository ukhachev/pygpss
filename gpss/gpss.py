class Gpss:
    def __init__(self, simulation_time):
        self._cec = []
        self._fec = []
        self._generators = []
        self._current_time = 0
        self._simulation_time = simulation_time

    def run(self, pipeline):
        self._input_phase(pipeline)
        # print('<html><table border="1"><th><td></td><td>ЦТС</td><td>ЦБС</td></th>')

        while self._current_time < self._simulation_time:
            self._adjust_timer()
            self._trace('После коррекции таймера')
            self._lookup()
            self._trace('После просмотра')
        # print('</table></html>')

    def _input_phase(self, pipeline):
        prev_block = None

        for cur_block in pipeline:
            generator = cur_block.get_generator()
            if generator:
                self._generators.append(generator)
            if prev_block:
                prev_block.set_next_block(cur_block)
            prev_block = cur_block

    def _adjust_timer(self):
        self._sort_by_moment(self._fec)
        self._generators.sort(key=lambda t: t.generate_moment)

        if not self._fec or self._fec[0].move_moment > self._generators[0].generate_moment:
            self._generate_new_transacts()

        self._current_time = self._fec[0].move_moment
        while self._fec and self._fec[0].move_moment == self._current_time:
            self._cec.append(self._fec[0])
            self._fec = self._fec[1:]

    def _lookup(self):
        while self._has_transacts_to_move():
            new_cec = []
            for transact in self._cec:
                prev_block = transact.current_block
                cur_block = transact.current_block.get_next_block(transact)
                # Продвигаем транзакт на столько болков, на сколько возможно
                while cur_block and cur_block.can_receive(transact, self._current_time):
                    prev_block.on_leave(transact, self._current_time)
                    transact.move_moment = self._current_time
                    transact.blocked = False
                    cur_block.receive_transact(transact, self._current_time)
                    transact.current_block = cur_block
                    # Помещаем транзакт в ЦБС
                    if transact.move_moment > self._current_time:
                        self._fec.append(transact)
                        break
                    prev_block = cur_block
                    cur_block = cur_block.get_next_block(transact)

                # Транзакт заблокирован. Помещаем в ЦТС
                if cur_block and not cur_block.can_receive(transact, self._current_time):
                    transact.blocked = True
                    new_cec.append(transact)
            self._cec = new_cec

    def _has_transacts_to_move(self):
        return any(map(lambda t: not t.blocked, self._cec))

    def _generate_new_transacts(self):
        self._current_time = self._generators[0].generate_moment
        for generator in self._generators:
            if generator.generate_moment != self._current_time:
                break
            self._fec.append(generator.get_next())
        self._sort_by_moment(self._fec)

    def _trace(self, prefix):
        pass

    def _sort_by_moment(self, event_chain):
        event_chain.sort(key=lambda t: t.move_moment)
