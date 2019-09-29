from slither.core.declarations.modifier import Modifier as Slither_Modifier
from slither.core.variables.state_variable import StateVariable as Slither_StateVariable
from slither.core.variables.variable import Variable as Slither_Variable
from .state_variable import StateVariable
from .variable import Variable
from slither.slithir.operations import SolidityCall
from slither.core.declarations import SolidityFunction
from .require import Require

require_functions = [SolidityFunction("require(bool)"),
                     SolidityFunction("require(bool,string)")]


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

    def update_local_variables(self):
        print(f'\tRemoving duplicates from Local Variables. ')
        for i, sv in enumerate(self.state_variables_read):
            for j, lv in enumerate(self.local_variables_read):
                if sv.name == lv.name:
                    del self.local_variables_read[j]

        for i, sv in enumerate(self.state_variables_written):
            for j, lv in enumerate(self.local_variables_written):
                if sv.name == lv.name:
                    del self.local_variables_written[j]

    def load_variables(self, modifier: Slither_Modifier, new_contract):
        for variable in modifier.state_variables_read:
            print(f'\tLoading State Variable Read: {variable.name}')
            if variable.name in new_contract.state_variables:
                new_variable = new_contract.state_variables[variable.name]
            else:
                new_variable = self.create_state_variable(variable)
                new_contract.state_variables[variable.name] = new_variable
            self.state_variables_read.append(new_variable)
            new_variable.modifiers_read.append(self)

        for variable in modifier.state_variables_written:
            print(f'\tLoading State Variable Wrote: {variable.name}')
            if variable.name in new_contract.state_variables:
                new_variable = new_contract.state_variables[variable.name]
            else:
                new_variable = self.create_state_variable(variable)
                new_contract.state_variables[variable.name] = new_variable
            self.state_variables_written.append(new_variable)
            new_variable.modifiers_written.append(self)

        for variable in modifier.variables_read:
            print(f'\tLoading Variable Read: {variable.name}')
            new_variable = self.create_variable(variable)
            self.local_variables_read.append(new_variable)

        for variable in modifier.variables_written:
            print(f'\tLoading Variable Wrote: {variable.name}')
            new_variable = self.create_variable(variable)
            self.local_variables_written.append(new_variable)

        self.update_local_variables()

        self.create_require(modifier)

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

    def create_require(self, modifier: Slither_Modifier):
        requires = modifier.all_slithir_operations()
        requires = [ir for ir in requires if isinstance(ir, SolidityCall) and ir.function in require_functions]
        requires = [ir.node for ir in requires]
        for require in requires:
            new_require = Require()
            self.requires.append(new_require)

            new_require.code = str(require.expression)
            print(f'\tAdding Require: {require.expression}')
            new_require.IRs = require.irs  # this still needs modification, IR class has not been created
            new_require.update_local_variables()
