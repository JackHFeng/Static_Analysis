
class Block:
    def __init__(self):
        # pc in int
        self.pc = None

        # start opcode pc, same as self.pc
        self.start = None

        # end opcode pc
        self.end = None

        # list of predecessors block pc in int
        self.pre = []

        # list of successors block pc in int
        self.next = []

    def info(self):
        return f'pc: {self.pc} [{self.start.pc}, {self.end.pc}]\n' \
               f'Predecessors: {self.pre}\n' \
               f'Successors: {self.next}\n'

    def __str__(self):
        return f'({self.start.pc}, {self.start.pc})'

    def __repr__(self):
        return f'({self.start.pc}, {self.start.pc})'
