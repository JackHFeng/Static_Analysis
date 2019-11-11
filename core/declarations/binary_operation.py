from .operation import Operation


class BinaryOperation(Operation):
    """
    This class is still yet to be utilized.
    Currently, we are using slither BinaryOperation directly
    """
    def __init__(self):
        super().__init__()
        self.left = None
        self.right = None
