from slither.core.variables.local_variable import LocalVariable as Slither_Local_Variable
from .local_variable import LocalVariable


class Parameter(LocalVariable):
    def __init__(self, variable: Slither_Local_Variable):
        """
        Still missing
        original count, count of rep values
        """
        super().__init__(variable)

        # list of representative values for the parameter
        self._rep_values = []

    @property
    def rep_values(self):
        return self._rep_values

    def load_rep_values(self, values):
        self._rep_values = values

    def get_w3_rep_value(self, index):
        from util import web3_value_encode
        return web3_value_encode(str(self.type), self.rep_values[index])

