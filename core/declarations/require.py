from slither.core.declarations.solidity_variables import SolidityVariableComposed as Slither_SolidityVariableComposed
from slither.core.expressions.binary_operation import BinaryOperation
from slither.core.expressions.identifier import Identifier
from slither.core.expressions.index_access import IndexAccess
from slither.core.expressions.literal import Literal
from slither.core.expressions.member_access import MemberAccess
from slither.core.expressions.tuple_expression import TupleExpression
from slither.core.expressions.unary_operation import UnaryOperation
from slither.slithir.variables.reference import ReferenceVariable
from slither.solc_parsing.cfg.node import NodeSolc as Solc_Node
from slither.solc_parsing.variables.local_variable import LocalVariableSolc
from slither.solc_parsing.variables.state_variable import StateVariableSolc

import utils
from .local_variable import LocalVariable
from .state_variable import StateVariable


class Require:
    """
    Require object for require statements.
    Only requires at the beginning of the functions and within modifiers have been created.

    *** To be completed.

    Cannot detect indirect read, but can detect indirect write, find out why.
    """

    def __init__(self, require: Solc_Node, parent_function_call):
        # from slither.slithir.variables.reference import ReferenceVariable
        # print(str(require.expression))
        # for var in require._slithir_vars:
        #     if isinstance(var, ReferenceVariable) and var.name == "REF_12":
        #         print(f'\t{var.name}  {type(var.points_to_origin)} {var.points_to_origin.name}   {type(var.points_to_origin.expression.expression_left.value)}')

        # original code of the require statement
        self._code = str(require.expression)

        # function where the require resides
        self._parent_function_call = parent_function_call

        # the intermediate representation of the require statement
        # so far has not been utilized
        self._irs = require.irs

        # local variables read by the require
        self._local_variables_read = set()

        # state variables read by the require
        self._state_variables_read = set()

        # flag for whether the require contain state variable
        self._contain_state_variable = False

        # slither expression of the operation within the require statement
        self._operation = require.expression.arguments[0]

        # 0 - Yet to be classified
        # 1 - Easiest, only require change of parameter
        #       Can be satisfied at anytime.
        # 2 - Medium, comparing state variable to its default value
        #       Can be satisfied after deployment.
        # 3 - Hard, require modification of state variables
        #       Require dependency information.
        # if all requires of a function are 1 or 2, then it can be fuzzed after deployment.
        self._sat_cond_class = 0  # Satisfying condition classification.

        self._load_variables(require)
        self.classify_sat_cond(require.expression.arguments[0])

    @property
    def code(self):
        return self._code

    @property
    def parent_function_call(self):
        return self._parent_function_call

    @property
    def irs(self):
        return self._irs

    @property
    def local_variables_read(self):
        return list(self._local_variables_read)

    @property
    def state_variables_read(self):
        return list(self._state_variables_read)

    @property
    def contain_state_variable(self):
        return self._contain_state_variable

    @property
    def operation(self):
        return self._operation

    @property
    def sat_cond_class(self):
        return self._sat_cond_class

    def compute_satisfying_condition(self):
        if len(self._state_variables_read) == 0:
            self._sat_cond_class = 1

    def classify_sat_cond(self, exp):
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
        utils.get_z3_vars(self._operation, z3_dic)

    def _get_all_identifiers(self, exp):
        """
        Get all the identifiers involved in an expression.

        *** may need to handle more operations.
        """
        res = []
        if not exp:
            return res
        elif isinstance(exp, Identifier):
            res.append(exp.value)
            return res
        elif isinstance(exp, Literal):
            return res
        elif isinstance(exp, BinaryOperation):
            res.extend(self._get_all_identifiers(exp.expression_left))
            res.extend(self._get_all_identifiers(exp.expression_right))
            return res
        elif isinstance(exp, UnaryOperation):
            res.extend(self._get_all_identifiers(exp.expression))
            return res
        elif isinstance(exp, TupleExpression):
            for e in exp.expressions:
                res.extend(self._get_all_identifiers(e))
            return res
        elif isinstance(exp, IndexAccess):
            res.extend(self._get_all_identifiers(exp.expression_left))
            res.extend(self._get_all_identifiers(exp.expression_right))
            return res
        elif isinstance(exp, MemberAccess):
            res.extend(self._get_all_identifiers(exp.expression))
            return res
        else:
            raise Exception(f'Unhandled solc operation type "{type(exp)}" for "{str(exp)}".')

    def _load_variables(self, require: Solc_Node):
        """
        Loads the state/local variable objects read by the require
        statement.
        """
        sv_read = []
        sv_read.extend(require.state_variables_read)
        v_read = []
        v_read.extend(require.variables_read)

        for ir_var in require.slithir_variables:
            if isinstance(ir_var, ReferenceVariable):
                origin = ir_var.points_to_origin
                additional_vars = self._get_all_identifiers(origin.expression)
                sv_read.extend([v for v in additional_vars if isinstance(v, StateVariableSolc)])
                v_read.extend(additional_vars)

        self._load_state_variables_read(sv_read)
        self._load_local_variables_read(v_read)

    def _load_state_variables_read(self, variables):
        """
        Loads the read state variable objects.
        """

        # this "variables" object consists of only slither state variable objects
        if variables:
            self._contain_state_variable = True
        for variable in variables:
            # print(f'Loading read state variable: {variable.name}')

            # if state variable object exists, using existing object
            # else, create a new one
            if variable.name in self._parent_function_call.parent_contract.state_variables:
                new_variable = self._parent_function_call.parent_contract.state_variables[variable.name]
            else:
                new_variable = StateVariable(variable)
                self._parent_function_call.parent_contract.state_variables[variable.name] = new_variable

            # adding current require to state variable
            new_variable.add_read_require(self)
            self._state_variables_read.add(new_variable)

    def _load_local_variables_read(self, variables):
        """
        Loads the read local variable objects.
        """

        # this "variables" object contains all variables read by the require statement
        # hence, contain both state, and local variables
        for variable in variables:
            if type(variable) not in [LocalVariableSolc, Slither_SolidityVariableComposed]:
                continue

            if variable.name in self._parent_function_call.local_variables:
                new_variable = self._parent_function_call.local_variables[variable.name]
            else:
                new_variable = LocalVariable(variable)
                self._parent_function_call.local_variables[variable.name] = new_variable

            self._local_variables_read.add(new_variable)

    def __str__(self):
        return self._code

    def __repr__(self):
        return self._code
