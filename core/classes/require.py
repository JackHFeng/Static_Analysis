from slither.solc_parsing.cfg.node import NodeSolc as Solc_Node


class Require:
    def __init__(self, require: Solc_Node, new_function):
        self.code = str(require.expression)
        self.from_function = new_function

        self.IRs = require.irs

        self.local_variables_read = []  # require doesn't write

        self.state_variables_read = []

        self.operation = require.expression.arguments[0]

        # def load_variables(self, require: Solc_Node):
        #     self.load_state_variables(function.state_variables_written, new_contract, 'written')
        #     self.load_local_variables(function.variables_written, 'written')
