from slither.solc_parsing.cfg.node import NodeSolc as Solc_Node
from slither.core.variables.state_variable import StateVariable as Slither_StateVariable
from slither.core.variables.local_variable import LocalVariable as Slither_Local_Variable
from .state_variable import StateVariable
from .variable import Variable


class Require:
    def __init__(self, require: Solc_Node, new_function):
        self.code = str(require.expression)
        self.from_function = new_function

        self.IRs = require.irs

        self.local_variables_read = []  # require doesn't write

        self.state_variables_read = []

        self.operation = require.expression.arguments[0]

    def load_variables(self, require: Solc_Node):
        self.load_state_variables(require.state_variables_read)
        self.load_local_variables(require.variables_read)

    def load_state_variables_read(self, variables: Slither_StateVariable):
        for variable in variables:
            print(f'Loading read state variable: {variable.name}')
            if variable.name in self.from_function.from_contract.state_variables:
                new_variable = self.from_function.from_contract.state_variables[variable.name]
            else:
                new_variable = StateVariable(variable)
                self.from_function.from_contract.state_variables[variable.name] = new_variable

            new_variable.requires_read.append(self)
            self.state_variables_read.append(new_variable)

    def load_local_variables_read(self, variables: Slither_Local_Variable):
        for variable in variables:
            print(f'Loading read local variable: {variable.name}')
            new_variable = Variable(variable)
            self.local_variables_read.append(new_variable)
