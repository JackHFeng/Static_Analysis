from slither.core.declarations.modifier import Modifier as Slither_Modifier
from slither.core.variables.state_variable import StateVariable as Slither_StateVariable
from slither.core.variables.variable import Variable as Slither_Variable
from .state_variable import StateVariable
from .variable import Variable


class Modifier:
    def __init__(self):
        self.name = ''
        self.visibility = ''

        self.state_variables_read = []
        self.state_variables_written = []  # Modifiers can write to state variables

        self.local_variables_read = []
        self.local_variables_written = []

        self.functions_used = []

        self.requires = []

    def get_state_variables_read(self):
        return self.state_variables_read

    def get_state_variables_written(self):
        return self.state_variables_written

    def get_local_variables_read(self):
        return self.local_variables_read

    def get_local_variables_written(self):
        return self.local_variables_written

    def get_requires(self):
        return self.requires

    def load_variables(self, modifier: Slither_Modifier, new_contract):
        for variable in modifier.state_variables_read:
            if variable.name in new_contract.state_variables:
                new_variable = new_contract.state_variables[variable.name]
            else:
                new_variable = self.create_state_variable(variable)
                new_contract.state_variables[variable.name] = new_variable
            self.state_variables_read.append(new_variable)
            new_variable.modifiers_read.append(self)

        for variable in modifier.state_variables_written:
            if variable.name in new_contract.state_variables:
                new_variable = new_contract.state_variables[variable.name]
            else:
                new_variable = self.create_state_variable(variable)
                new_contract.state_variables[variable.name] = new_variable
            self.state_variables_written.append(new_variable)
            new_variable.modifiers_written.append(self)

        for variable in modifier.variables_read:
            new_variable = self.create_variable(variable)
            self.local_variables_read.append(new_variable)

        for variable in modifier.variables_written:
            new_variable = self.create_variable(variable)
            self.local_variables_written.append(new_variable)

    def create_state_variable(self, variable: Slither_StateVariable) -> StateVariable:
        new_variable = StateVariable()
        new_variable.name = variable.name
        new_variable.type = variable.type
        new_variable.visibility = variable.visibility
        new_variable.initialized = variable.initialized
        return new_variable

    def create_variable(self, variable: Slither_Variable) -> Variable:
        new_variable = Variable
        new_variable.name = variable.name
        new_variable.type = variable.type
        return new_variable
