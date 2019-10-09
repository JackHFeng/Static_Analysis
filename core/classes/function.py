from slither.core.declarations.function import Function as Slither_Function
from slither.core.variables.state_variable import StateVariable as Slither_StateVariable
from slither.core.variables.local_variable import LocalVariable as Slither_Local_Variable
from .variable import Variable
from .state_variable import StateVariable
from slither.slithir.operations import SolidityCall
from slither.core.declarations import SolidityFunction
from .require import Require
from slither.core.expressions.binary_operation import BinaryOperation
from slither.core.expressions.unary_operation import UnaryOperation
from slither.solc_parsing.cfg.node import NodeSolc as Solc_Node

require_functions = [SolidityFunction("require(bool)"),
                     SolidityFunction("require(bool,string)")]


class Function:
    def __init__(self, function: Slither_Function, new_contract):
        self.name = function.name
        self.signature = function.signature_str
        self.visibility = function.visibility
        self.from_contract = new_contract

        self.modifiers = []

        self.requires = []

        self.state_variables_written = []
        self.state_variables_read = []

        self.local_variables_read = []
        self.local_variables_written = []

        print(f'Creating Function: {function.name}')

        self.load_variables(function, new_contract)

    def load_variables(self, function: Slither_Function, new_contract):
        self.load_state_variables(function.state_variables_written, new_contract, 'written')
        self.load_local_variables(function.variables_written, 'written')

        self.load_requires(function, new_contract)

    def load_state_variables(self, variables: Slither_StateVariable, new_contract, RorW):
        for variable in variables:
            print(f'Loading {RorW} state variable: {variable.name}')
            if variable.name in new_contract.state_variables:
                new_variable = new_contract.state_variables[variable.name]
            else:
                new_variable = StateVariable(variable)
                new_contract.state_variables[variable.name] = new_variable
            getattr(new_variable, self.__class__.__name__.lower() + 's_' + RorW).append(self)
            getattr(self, 'state_variables_' + RorW).append(new_variable)
            getattr(new_variable, 'functions_' + RorW).append(self)

    def load_local_variables(self, variables: Slither_Local_Variable, RorW):
        for variable in variables:
            if variable.name not in [v.name for v in getattr(self, 'state_variables_' + RorW)]:
                print(f'Loading {RorW} local variable: {variable.name}')
                new_variable = Variable(variable)
                getattr(self, 'local_variables_' + RorW).append(new_variable)

    def load_requires(self, function: Slither_Function, new_contract):
        requires = function.all_slithir_operations()
        requires = [ir for ir in requires if isinstance(ir, SolidityCall) and ir.function in require_functions]
        requires = [ir.node for ir in requires]

        for require in requires:
            self.create_require(require, new_contract)

    def create_require(self, require: Solc_Node, new_contract):
        self.load_state_variables(require.state_variables_read, new_contract, 'read')
        self.load_local_variables(require.variables_read, 'read')
        print(f'Creating Require object: {str(require.expression)}')
        new_require = Require(require, self)

        self.requires.append(new_require)

        # print(f'\t@@@@Adding Require: {require.expression}')
        # if type(require.expression.arguments[0]) == BinaryOperation:
        #     print(f'\tleft: {require.expression.arguments[0].expression_left}, right: {require.expression.arguments[0].expression_right}, operation: {require.expression.arguments[0].type_str}')
        #     print(type(require.expression.arguments[0].expression_right))
        #     print(require.expression.arguments[0].expression_right.type)
        # elif type(require.expression.arguments[0]) == UnaryOperation:
        #     print(
        #         f'\texpression: {require.expression.arguments[0].expression}, operation: {require.expression.arguments[0].type_str}')
