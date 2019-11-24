from slither.solc_parsing.cfg.node import NodeSolc as Solc_Node
from .state_variable import StateVariable
from .variable import Variable




from slither.core.expressions.binary_operation import BinaryOperation
from slither.core.expressions.unary_operation import UnaryOperation
from slither.core.expressions.tuple_expression import TupleExpression
from slither.core.expressions.identifier import Identifier
from slither.core.expressions.literal import Literal
import utils

from slither.core.variables.state_variable import StateVariable as Slither_StateVariable
from slither.core.variables.local_variable import LocalVariable as Slither_LocalVariable
from slither.core.declarations.solidity_variables import SolidityVariableComposed as Slither_SolidityVariableComposed


class Require:
    """
    Require object for require statements.
    Only requires at the beginning of the functions and within modifiers have been created.

    *** To be completed.

    Cannot detect indirect read, but can detect indirect write, find out why.
    """

    def __init__(self, require: Solc_Node, new_function):
        # original code of the require statement
        self.code = str(require.expression)

        # function where the require resides
        self.from_function = new_function

        # the intermediate representation of the require statement
        # so far has not been utilized
        self.IRs = require.irs

        # local variables read by the require
        self.local_variables_read = set()

        # state variables read by the require
        self.state_variables_read = set()

        # flag for whether the require contain state variable
        self.contain_state_variable = False

        # slither expression of the operation within the require statement
        self.operation = require.expression.arguments[0]

        # 0 - Yet to be classified
        # 1 - Easiest, only require change of parameter
        # 2 - Medium, comparing state variable to its default value
        # 3 - Hard, require modification of state variables
        self.satisfying_condition = 0

        self.load_variables(require)
        self.classify_require(require.expression.arguments[0])



    def compute_satisfying_condition(self):
        if len(self.state_variables_read) == 0:
            self.satisfying_condition = 1

    def classify_require(self, exp):
        """
        This is for checking classifications of require.
        *** Still needs modification.
        """
        if isinstance(exp, BinaryOperation):
            pass
            # for e in exp.expressions:
            #     print(f'{str(e)}: {type(e)}')
        elif isinstance(exp, UnaryOperation):
            e = exp.expression
            # print(f'{str(e)}: {type(e)}')
        elif isinstance(exp, Literal) or isinstance(exp, Identifier):
            # print(f'{str(exp)}: {type(exp)}')
            pass
        else:
            # print(f'{str(exp)}: {str(exp)}')
            self.is_simple_require = False

    def evaluate_require_satisfiability(self):
        z3_dic = {}
        utils.get_z3_vars(self.operation, z3_dic)

    def load_variables(self, require: Solc_Node):
        """
        Loads the state/local variable objects read by the require
        statement.
        """
        self.load_state_variables_read(require.state_variables_read)
        self.load_local_variables_read(require.variables_read)

    def load_state_variables_read(self, variables):
        """
        Loads the read state variable objects.
        """

        # this "variables" object consists of only slither state variable objects
        if variables:
            self.contain_state_variable = True
        for variable in variables:
            # print(f'Loading read state variable: {variable.name}')

            # if state variable object exists, using existing object
            # else, create a new one
            if variable.name in self.from_function.from_contract.state_variables:
                new_variable = self.from_function.from_contract.state_variables[variable.name]
            else:
                new_variable = StateVariable(variable)
                self.from_function.from_contract.state_variables[variable.name] = new_variable

            # adding current require to state variable
            new_variable.requires_read.add(self)
            self.state_variables_read.add(new_variable)

    def load_local_variables_read(self, variables):
        """
        Loads the read local variable objects.
        """

        # this "variables" object contains all variables read by the require statement
        # hence, contain both state, and local variables
        for variable in variables:
            if type(variable) not in [Slither_StateVariable, Slither_LocalVariable, Slither_SolidityVariableComposed]:
                continue
            # only loads non-state variables into the "self.local_variables_read" object
            if variable and variable.name not in [v.name for v in self.state_variables_read]:
                # print(f'Loading read local variable: {variable.name}')
                new_variable = Variable(variable)
                self.local_variables_read.add(new_variable)

    def __str__(self):
        return self.code

    def __repr__(self):
        return self.code


