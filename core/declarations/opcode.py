class Opcode:
    def __init__(self):
        self.pc = None
        self.opcode = None
        self.size = None
        self.value = None

        self.pre = None
        self.next = None

    def __str__(self):
        return f'{self.pc} {self.opcode} {self.value if self.value else ""}'
