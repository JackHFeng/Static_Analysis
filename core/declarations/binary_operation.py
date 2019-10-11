from .operation import Operation


class BinaryOperation(Operation):
    def __init__(self):
        super().__init__()
        self.left = None
        self.right = None
