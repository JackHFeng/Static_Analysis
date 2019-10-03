from slither.core.declarations.function import Function as Slither_Function
from slither.core.variables.state_variable import StateVariable as Slither_StateVariable
from slither.core.variables.variable import Variable as Slither_Variable
from .variable import Variable
from .state_variable import StateVariable
from slither.slithir.operations import SolidityCall
from slither.core.declarations import SolidityFunction
from .require import Require
from slither.core.expressions.binary_operation import BinaryOperation
from slither.core.expressions.unary_operation import UnaryOperation

require_functions = [SolidityFunction("require(bool)"),
                     SolidityFunction("require(bool,string)")]


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
        print(f'\tRemoving duplicates from Local Variables. ')
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
            print(f'\tLoading State Variable Read {variable.name}')
            if variable.name in new_contract.state_variables:
                new_variable = new_contract.state_variables[variable.name]
            else:
                new_variable = self.create_state_variable(variable)
                new_contract.state_variables[variable.name] = new_variable
            self.state_variables_read.append(new_variable)
            new_variable.functions_read.append(self)

        for variable in function.state_variables_written:
            print(f'\tLoading State Variable Wrote: {variable.name}')
            if variable.name in new_contract.state_variables:
                new_variable = new_contract.state_variables[variable.name]
            else:
                new_variable = self.create_state_variable(variable)
                new_contract.state_variables[variable.name] = new_variable
            self.state_variables_written.append(new_variable)
            new_variable.functions_written.append(self)

        #print(f'{function.variables_read}')
        for variable in function.variables_read:
            if not variable: continue
            print(f'\tLoading Variable Read: {variable.name}')
            new_variable = self.create_variable(variable)
            self.local_variables_read.append(new_variable)

        for variable in function.variables_written:
            print(f'\tLoading Variable Wrote: {variable.name}')
            new_variable = self.create_variable(variable)
            self.local_variables_written.append(new_variable)

        self.update_local_variables()

        self.create_require(function)

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
        #new_variable.type = variable.type
        return new_variable

    def create_require(self, function: Slither_Function):
        requires = function.all_slithir_operations()
        requires = [ir for ir in requires if isinstance(ir, SolidityCall) and ir.function in require_functions]
        requires = [ir.node for ir in requires]
        for require in requires:
            new_require = Require()
            self.requires.append(new_require)

            new_require.code = str(require.expression)
            print(f'\t@@@@Adding Require: {require.expression}')
            if type(require.expression.arguments[0]) == BinaryOperation:
                print(f'\tleft: {require.expression.arguments[0].expression_left}, right: {require.expression.arguments[0].expression_right}, operation: {require.expression.arguments[0].type_str}')
                print(type(require.expression.arguments[0].expression_right))
                print(require.expression.arguments[0].expression_right.type)
            elif type(require.expression.arguments[0]) == UnaryOperation:
                print(
                    f'\texpression: {require.expression.arguments[0].expression}, operation: {require.expression.arguments[0].type_str}')
            new_require.IRs = require.irs  # this still needs modification, IR class has not been created
            new_require.operation = require.expression.arguments[0]
            new_require.update_local_variables()

