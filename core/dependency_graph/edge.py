from core.declarations.function import Function


class Edge:
    def __init__(self, _head: Function, _tail: Function):
        self.head = _head.name
        self.tail = _tail.name
