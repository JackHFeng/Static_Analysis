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

    Notes:
        1.
            slither built-in functions, state_variables_read, state_variables_written only detects the requires,
            state variables that directly appear in the function. If they reside within another function call, or
            in a modifier, the built-in functions will not be able to detect them.

            However, IR that is used in this implementation will detect all indirect requires and state variables.

            We have to be very cautious on which approach we should take.

            *** Currently, we are computing the "read by require" correctly, because we are using IR to find the require
                statements and taking out all the state variables from it.

                However, if a state variable is indirectly written, our current implementation will not detect it.
                Switching to IR will help, be at this moment, it may be of lower priority.

        2.
            Modifiers can modify state variables. While the state variables written by the modifier are loaded in the
            function object, it is still yet to be determined on what to do with it.

            Modifiers can take input parameters as well.

    *** To be completed.
    """
    def __init__(self, _function: Slither_Function, _parent_contract):

        # e.g. "constructor".
        self.name = _function.name

        # e.g. "constructor(bytes32[]) returns()".
        self.signature = _function.signature_str

        # e.g. "public", "external", "internal", etc.
        self.visibility = _function.visibility

        # contract object where current function belongs.
        self.from_contract = _parent_contract

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

        self.load_parameters(_function)
        self.load_variables(_function)
        self.load_requires(_function)
        self.load_modifiers(_function)

        # if the current function is the constructor,
        # we update all the state variables that are written by the constructor.
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

    def get_depended_functions_by_state_variable(self, _name):
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
            if sv.name == _name:
                for fn in sv.functions_written:
                    if fn is not self and fn not in res and fn.visibility == 'public':
                        res.append(fn)
                return res

        return res
        # throw exception? Or just return empty array?
        # Exception(f'The current function "{self.name}" does not read state variable "{name}".')

    def load_parameters(self, _function: Slither_Function):
        """
        Creating the parameter objects.

        Finished.
        """
        for variable in _function.parameters:
            new_variable = Variable(variable)
            self.parameters.add(new_variable)

    def load_variables(self, _function: Slither_Function):
        """
        Loading both local and state variable objects.

        Finished.
        """
        self.load_state_variables(_function.state_variables_written, 'written')
        self.load_local_variables(_function.variables_written, 'written')

    def load_state_variables(self, _variables: Slither_StateVariable, _RorW):
        """
        Loading state variable objects.

        Finished.
        """
        for variable in _variables:
            #print(f'Loading {RorW} state variable: {variable.name}')
            if variable.name in self.from_contract.state_variables:
                new_variable = self.from_contract.state_variables[variable.name]
            else:
                new_variable = StateVariable(variable)
                self.from_contract.state_variables[variable.name] = new_variable
            getattr(new_variable, self.__class__.__name__.lower() + 's_' + _RorW).add(self)
            getattr(self, 'state_variables_' + _RorW).add(new_variable)

    def load_local_variables(self, _variables: Slither_Local_Variable, _RorW):
        """
        Loading local variable object.

        Finished.
        """
        for variable in _variables:
            if variable and variable.name not in [v.name for v in getattr(self, 'state_variables_' + _RorW)]:
                #print(f'Loading {RorW} local variable: {variable.name}')
                new_variable = Variable(variable)
                getattr(self, 'local_variables_' + _RorW).add(new_variable)

    def load_requires(self, _function: Slither_Function):
        """
        Loading require objects.

        Notes:
            Requires from both modifier and calls to another function will be added.
                How should require from another function be treated?

            We need to differentiate requires that are not pre-conditions.
                Either requires that does not appear at the beginning of the function call, or post condition modifiers.
                This maybe easily achieved by using IR.

            However, some requires might not appear at the beginning, yet they are still checking the pre-condition.
                e.g.
                    sender = msg.sender;
                    require(owner == sender);

        *** To be completed.
            Remove post condition requires.


        """
        print(f"*******{self.name}")
        from slither.slithir.operations.internal_call import InternalCall
        for n in _function.nodes:
            print(f'node: {n}')
            for ir in n.irs:
                print(f'\t ir: {ir} {type(ir)}')
                if isinstance(ir, InternalCall):
                    for nn in ir.function.nodes:

                        print(f'\t\t {nn}')
        print("*****")
        requires = _function.all_slithir_operations()
        temp = []
        # print(f"*******{self.name}")
        # for ir in requires:
        #     print(f'\t{ir}  {type(ir)} ')
        # print("*****")
        requires = [ir for ir in requires if isinstance(ir, SolidityCall) and ir.function in require_functions]
        requires = [ir.node for ir in requires]

        for require in requires:
            # print(f'{self.name} {require}')
            self.create_require(require)

    def create_require(self, _require: Solc_Node):
        self.load_state_variables(_require.state_variables_read, 'read')
        self.load_local_variables(_require.variables_read, 'read')
        new_require = Require(_require, self)

        self.requires.add(new_require)

        for state_variable in new_require.state_variables_read:
            if state_variable not in self.state_variables_read:
                self.state_variables_read.add(state_variable)

    def load_modifiers(self, _function: Slither_Function):
        for modifier in _function.modifiers:
            self.modifiers.add(self.from_contract.modifiers[modifier.name])
            for state_variable in self.from_contract.modifiers[modifier.name].state_variables_written:
                self.state_variables_written.add(state_variable)
            for state_variable in self.from_contract.modifiers[modifier.name].state_variables_read:
                self.state_variables_read.add(state_variable)
            # for require in self.from_contract.modifiers[modifier.name].requires:
            #     self.requires.append(require)

    def __str__(self):
        return self.signature


# static utility functions

def load_irs(_node, _ir_list):
    pass
