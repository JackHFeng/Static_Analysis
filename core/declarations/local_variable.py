from slither.core.variables.local_variable import LocalVariable as Slither_Local_Variable

from .variable import Variable


class LocalVariable(Variable):
    def __init__(self, variable: Slither_Local_Variable):
        super().__init__(variable)
        self._name = variable.name
        self._type = variable.type

