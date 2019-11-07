from slither.solc_parsing.cfg.node import NodeSolc as Solc_Node
from slither.core.variables.state_variable import StateVariable as Slither_StateVariable
from slither.core.variables.local_variable import LocalVariable as Slither_Local_Variable
from .state_variable import StateVariable
from .variable import Variable
from slither.core.expressions.literal import Literal
from slither.core.expressions.identifier import Identifier
from slither.core.expressions.binary_operation import BinaryOperation
from slither.core.expressions.unary_operation import UnaryOperation


class Require:
    def __init__(self, require: Solc_Node, new_function):
        self.code = str(require.expression)
        self.from_function = new_function

        self.IRs = require.irs

        self.local_variables_read = set()  # require doesn't write

        self.state_variables_read = set()
        self.contain_state_variable = False

        self.operation = require.expression.arguments[0]

        self.calculation_complexity = 0

        self.load_variables(require)
        self.check_simple_require(require.expression.arguments[0])



    def check_simple_require(self, exp):
        if isinstance(exp, BinaryOperation):
            pass
            # for e in exp.expressions:
            #     print(f'{str(e)}: {type(e)}')
        elif isinstance(exp, UnaryOperation):
            e = exp.expression
            #print(f'{str(e)}: {type(e)}')
        elif isinstance(exp, Literal) or isinstance(exp, Identifier):
            #print(f'{str(exp)}: {type(exp)}')
            pass
        else:
            #print(f'{str(exp)}: {str(exp)}')
            self.is_simple_require = False

    def load_variables(self, require: Solc_Node):
        self.load_state_variables_read(require.state_variables_read)
        self.load_local_variables_read(require.variables_read)

    def load_state_variables_read(self, variables: Slither_StateVariable):
        if variables:
            self.contain_state_variable = True
        for variable in variables:
            print(variable.name)
            print(variable.expression)
            #print(f'Loading read state variable: {variable.name}')
            if variable.name in self.from_function.from_contract.state_variables:
                new_variable = self.from_function.from_contract.state_variables[variable.name]
            else:
                new_variable = StateVariable(variable)
                self.from_function.from_contract.state_variables[variable.name] = new_variable

            new_variable.requires_read.add(self)
            self.state_variables_read.add(new_variable)

    def load_local_variables_read(self, variables: Slither_Local_Variable):
        for variable in variables:
            if variable and variable.name not in [v.name for v in self.state_variables_read]:
                #print(f'Loading read local variable: {variable.name}')
                new_variable = Variable(variable)
                self.local_variables_read.add(new_variable)
