from static_analysis.declarations.function import Function


class Edge:
    def __init__(self, _head: Function, _tail: Function):
        self.head = _head._name
        self.tail = _tail._name
