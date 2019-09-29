from slither.core.declarations.function import Function as Slither_Function
from slither.core.variables.state_variable import StateVariable as Slither_StateVariable
from slither.core.variables.variable import Variable as Slither_Variable
from .variable import Variable
from .state_variable import StateVariable


class Function:
    def __init__(self):
        self.name = ''
        self.signature = ''
        self.visibility = ''

        self.state_variables_written = []
        self.state_variables_read = []

        self.modifiers = []

        self.requires = []

        self.local_variables_read = []
        self.local_variables_written = []

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

    def update_local_variables(self):
        for i, sv in enumerate(self.state_variables_read):
            for j, lv in enumerate(self.local_variables_read):
                if sv.name == lv.name:
                    del self.local_variables_read[j]

        for i, sv in enumerate(self.state_variables_written):
            for j, lv in enumerate(self.local_variables_written):
                if sv.name == lv.name:
                    del self.local_variables_written[j]

    def load_variables(self, function: Slither_Function, new_contract):
        for variable in function.state_variables_read:
            if variable.name in new_contract.state_variables:
                new_variable = new_contract.state_variables[variable.name]
            else:
                new_variable = self.create_state_variable(variable)
                new_contract.state_variables[variable.name] = new_variable
            self.state_variables_read.append(new_variable)
            new_variable.functions_read.append(self)

        for variable in function.state_variables_written:
            if variable.name in new_contract.state_variables:
                new_variable = new_contract.state_variables[variable.name]
            else:
                new_variable = self.create_state_variable(variable)
                new_contract.state_variables[variable.name] = new_variable
            self.state_variables_written.append(new_variable)
            new_variable.functions_written.append(self)

        for variable in function.variables_read:
            new_variable = self.create_variable(variable)
            self.local_variables_read.append(new_variable)

        for variable in function.variables_written:
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
        new_variable = Variable()
        new_variable.name = variable.name
        new_variable.type = variable.type
        return new_variable
