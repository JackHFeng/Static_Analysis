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

# types of require function calls for getting the list of requires.
require_functions = [SolidityFunction("require(bool)"),
                     SolidityFunction("require(bool,string)")]


class Function:
    """
    Function objects

    It can find all requires and variables read by the requires because the analysis came from IR.


    *** To be completed.
        What if the current function calls another function?
            Will the state variable read/written show up if they are accessed in that function?
            What about require?
            What about modifier?
    """
    def __init__(self, function: Slither_Function, new_contract):

        # e.g. "constructor".
        self.name = function.name

        # e.g. "constructor(bytes32[]) returns()".
        self.signature = function.signature_str

        # e.g. "public", "external", "internal", etc.
        self.visibility = function.visibility

        # contract object where current function belongs.
        self.from_contract = new_contract

        # set of modifiers.
        self.modifiers = set()

        # set of requires.
        self.requires = set()

        # set of parameters.
        self.parameters = set()

        # set of state variables written by the function.
        self.state_variables_written = set()

        # set of state variables read by the function.
        # specifically, read by the requires within the function.
        self.state_variables_read = set()

        # local variables read by the function.
        self.local_variables_read = set()
        self.local_variables_written = set()

        # print(f'Creating Function: {function.name}')

        self.load_parameters(function)
        self.load_variables(function)
        self.load_requires(function)
        self.load_modifiers(function)

        # if the current function is the constructor.
        # update all the state variables that are written by the constructor.
        # change their .set_by_constructor to True
        if self.name == "constructor":
            for sv in self.state_variables_written:
                sv.set_by_constructor = True

        #print(f'{self.name}  {str(self.state_variables_written)}  {self.state_variables_read}')

    def get_depended_functions(self):
        """
        Returns the list of functions the current function depends on.
        The data dependency here is all the state variables that the current function reads.

        *** To be completed.
            Cases where the returned array might be empty.
                What if the current function does not read any state variable?
                What if none of the read state variables cannot be modified by another function?
        """
        res = []
        for sv in self.state_variables_read:
            for fn in sv.functions_written:
                if fn is not self and fn not in res and fn.visibility == 'public':
                    res.append(fn)
        return res

    def get_depended_functions_by_state_variable(self, name):
        """
        Returns the list of functions the current function depends on.
        The data dependency here is the specified state variables that the current function reads.

        *** To be completed.
            Cases where the returned array might be empty.
                What if the current function does not read any state variable?
                What if the specified read state variables cannot be modified by another function?
        """
        res = []
        for sv in self.state_variables_read:
            if sv.name == name:
                for fn in sv.functions_written:
                    if fn is not self and fn not in res and fn.visibility == 'public':
                        res.append(fn)
                return res

        Exception(f'The current function "{self.name}" does not read state variable "{name}".')

    def load_parameters(self, function: Slither_Function):
        """
        Creating the parameter objects.

        Finished.
        """
        for variable in function.parameters:
            new_variable = Variable(variable)
            self.parameters.add(new_variable)

    def load_variables(self, function: Slither_Function):
        """
        Loading both local and state variable objects.

        Finished.
        """
        self.load_state_variables(function.state_variables_written, 'written')
        self.load_local_variables(function.variables_written, 'written')

    def load_state_variables(self, variables: Slither_StateVariable, RorW):
        """
        Loading state variable objects.
        """
        # if a state variable is written in the modifier, this is currently not supported.
        for variable in variables:
            #print(f'Loading {RorW} state variable: {variable.name}')
            if variable.name in self.from_contract.state_variables:
                new_variable = self.from_contract.state_variables[variable.name]
            else:
                new_variable = StateVariable(variable)
                self.from_contract.state_variables[variable.name] = new_variable
            getattr(new_variable, self.__class__.__name__.lower() + 's_' + RorW).add(self)
            getattr(self, 'state_variables_' + RorW).add(new_variable)

    def load_local_variables(self, variables: Slither_Local_Variable, RorW):
        for variable in variables:
            if variable and variable.name not in [v.name for v in getattr(self, 'state_variables_' + RorW)]:
                #print(f'Loading {RorW} local variable: {variable.name}')
                new_variable = Variable(variable)
                getattr(self, 'local_variables_' + RorW).add(new_variable)

    def load_requires(self, function: Slither_Function):
        """
        *** To be completed.
            Currently ,if a require is within a function that the current function calls, that require is gonna show up as well.
        """

        requires = function.all_slithir_operations()
        requires = [ir for ir in requires if isinstance(ir, SolidityCall) and ir.function in require_functions]
        requires = [ir.node for ir in requires]

        for require in requires:
            #print(f'{self.name} {require}')
            self.create_require(require)

    def create_require(self, require: Solc_Node):
        self.load_state_variables(require.state_variables_read, 'read')
        self.load_local_variables(require.variables_read, 'read')
        new_require = Require(require, self)

        self.requires.add(new_require)

        for state_variable in new_require.state_variables_read:
            if state_variable not in self.state_variables_read:
                self.state_variables_read.add(state_variable)

    def load_modifiers(self, function: Slither_Function):
        for modifier in function.modifiers:
            self.modifiers.add(self.from_contract.modifiers[modifier.name])
            for state_variable in self.from_contract.modifiers[modifier.name].state_variables_written:
                if state_variable in self.state_variables_written:
                    pass
                    #print("already there written.")
                self.state_variables_written.add(state_variable)
            for state_variable in self.from_contract.modifiers[modifier.name].state_variables_read:
                if state_variable in self.state_variables_read:
                    pass
                    #print("already there read.")
                self.state_variables_read.add(state_variable)
            # for require in self.from_contract.modifiers[modifier.name].requires:
            #     self.requires.append(require)

    def __str__(self):
        return self.signature
