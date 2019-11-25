from typing import List

from .variable import Variable
from .state_variable import StateVariable
from .require import Require

from slither.core.declarations.function import Function as Slither_Function
from slither.core.variables.state_variable import StateVariable as Slither_StateVariable
from slither.core.variables.local_variable import LocalVariable as Slither_LocalVariable
from slither.slithir.operations import SolidityCall as Slither_SolidityCall
from slither.core.declarations import SolidityFunction as Slither_SolidityFunction
from slither.solc_parsing.cfg.node import NodeSolc as Slither_NodeSolc
from slither.slithir.operations.internal_call import InternalCall as Slither_InternalCall
from slither.solc_parsing.declarations.function import FunctionSolc as Slither_FunctionSolc
from slither.core.declarations.solidity_variables import SolidityVariableComposed as Slither_SolidityVariableComposed
from slither.solc_parsing.variables.state_variable import StateVariableSolc
from slither.solc_parsing.variables.local_variable import LocalVariableSolc
# types of require function calls for getting the list of requires.
require_functions = [Slither_SolidityFunction("require(bool)"),
                     Slither_SolidityFunction("require(bool,string)")]


class Function:
    """
    Function objects

    Notes:
        1.
            ❌slither built-in functions, state_variables_read, state_variables_written only detects the requires,
            state variables that directly appear in the function. If they reside within another function call, or
            in a modifier, the built-in functions will not be able to detect them.

            However, IR that is used in this implementation will detect all indirect requires and state variables.

            We have to be very cautious on which approach we should take.

            ✔*** Currently, we are computing the "read by require" correctly, because we are using IR to find the require
                statements and taking out all the state variables from it.

            ✔*** However, if a state variable is indirectly written, our current implementation will not detect it.
                Switching to IR will help, but at this moment, it may be of lower priority.

            ❌*** Require indirect read of state/local variable is also not supported at the moment.

        2.
            ❌*** Modifiers can modify state variables. While the state variables written by the modifier are loaded in the
            Function object of our design, it is still yet to be determined on what to do with it.

            Modifiers can take input parameters as well.

            Modifiers can call another function within itself....😒

            Modifier can be used to check both pre-condition or post-condition
            And a single modifier can check both pre-condition and post-condition at the same time....😒

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

        # list of IRs
        # we may not need this after all.
        self.ir_list = []

        # set of requires.
        self.requires = set()

        # set of parameters.
        self.parameters = set()

        # source code of function, currently not available
        self.source_code = ''

        # whether the function is view type
        self.is_view = True if _function.view else False

        # whether the function is pure type
        self.is_pure = True if _function.pure else False

        # set of state variables written by the function.
        self.state_variables_written = set()

        # set of state variables read by the function.
        # specifically, read by the requires within the function.
        self.state_variables_read = set()

        # local variables read by the function.
        self.local_variables_read = set()
        self.local_variables_written = set()

        # print(f'Creating Function: {function.name}')

        # load parameters.
        self.load_parameters(_function)

        # load both local and state variables.
        self.load_variables(_function)

        # we may not need this after all.
        # self.load_irs(_function.nodes)

        # load modifier objects.
        # requires within modifiers will be loaded into self.requires as well.
        self.load_modifiers(_function)

        # load requires at the front of the function.
        self.load_function_requires(_function)

        # if the current function is the constructor,
        # we update all the state variables that are written by the constructor.
        # change their .set_by_constructor to True
        if self.name == "constructor":
            for sv in self.state_variables_written:
                sv.set_by_constructor = True

        # print(f'{self.name} {self.requires}')

    def get_depended_functions(self):
        """
        Returns the list of functions the current function depends on.
        The data dependency here is all the state variables that the current function reads.

        Notes:
            Cases where the returned array might be empty.
                What if the current function does not read any state variable?
                What if none of the read state variables can be modified by another function?

        Finished.
        """
        res = []
        for sv in self.state_variables_read:
            for fn in sv.functions_written:
                # only returns public functions
                if fn is not self and fn not in res and fn.visibility == 'public':
                    res.append(fn)
        return res

    def get_depended_functions_by_state_variable(self, _name):
        """
        Returns the list of functions the current function depends on.
        The data dependency here is the specified state variables that the current function reads.

        Notes:
            Cases where the returned array might be empty.
                What if the current function does not read any state variable?
                What if none of the read state variables can be modified by another function?

        Finished.
        """
        res = []
        for sv in self.state_variables_read:
            if sv.name == _name:
                for fn in sv.functions_written:
                    # only returns public functions
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
            # get from dict if already exist
            if variable.name in self.from_contract.state_variables:
                new_variable = self.from_contract.state_variables[variable.name]
            else:
                new_variable = StateVariable(variable)
                self.from_contract.state_variables[variable.name] = new_variable
            getattr(new_variable, self.__class__.__name__.lower() + 's_' + _RorW).add(self)
            getattr(self, 'state_variables_' + _RorW).add(new_variable)

    def load_local_variables(self, _variables: Slither_LocalVariable, _RorW):
        """
        Loading local variable object.

        Finished.
        """
        for variable in _variables:
            # Slither_SolidityVariableComposed is msg.send etc.
            # There can be other types such as
            #       slither.solc_parsing.variables.local_variable_init_from_tuple.LocalVariableInitFromTupleSolc
            #           (Refer to slither def)
            #       slither.core.declarations.solidity_variables.SolidityVariable (now)
            if type(variable) not in [StateVariableSolc, LocalVariableSolc, Slither_SolidityVariableComposed]:
                continue
            # There was a check of whether "variable" is None in the if condition
            # But has been removed.

            # duplicate has been checked.
            if variable.name not in [v.name for v in getattr(self, 'state_variables_' + _RorW)]\
                    and variable.name not in [v.name for v in getattr(self, 'local_variables_' + _RorW)]:
                new_variable = Variable(variable)
                getattr(self, 'local_variables_' + _RorW).add(new_variable)

    def load_function_requires(self, _function):
        """
        Loading front require objects in a function.

        Notes:
            ✔What about requires from calls to another function?
                ✔*** This is currently not considered since they are not the pre-conditional requires of the parent
                    function.

            ❌We need to differentiate requires that are not pre-conditions.
                Either requires that does not appear at the beginning of the function call, or post condition modifiers.
                This maybe achieved by using IR.
                    ✔*** requires doesn't appear at the beginning of the function call as been removed.
                    ❌*** post-conditional requires from modifiers due to _; still needs to be removed.

            ✔However, some requires might not appear at the beginning, yet they are still checking the pre-condition.
            ❌This is also indirect read of variables, which has not been handled.
                e.g.
                    sender = msg.sender;
                    require(owner == sender);
        """
        for node in _function.nodes:
            # https://github.com/crytic/slither/blob/master/slither/core/cfg/node.py
            # node_type => 0 represents Entry Point Node, we can safely skip this.
            # node_type => 19 (0x13 in hex) represents Variable Declaration, we can safely skip this because
            # requires appears after new variable declaration should still be pre-condition checking.
            if node._node_type in [0, 19]:
                continue

            # require() is a internal call, this finds potential require statement.
            if node.internal_calls:
                # check if the call is actually require call.
                if node.internal_calls[0] in require_functions:
                    self.create_require(node)
                else:
                    # if not. Requires appear after this are not pre-conditional checking requires.
                    break
            else:
                # if not. Requires appear after this are not pre-conditional checking requires.
                break

    def load_modifier_requires(self, _modifier):
        """
        Loading require objects in a modifier.

        *** To be completed.
            Currently this is treating all requires in modifiers as pre-conditions.
            We need to remove post-condition
        """
        for ir in _modifier.slithir_operations:
            if isinstance(ir, Slither_SolidityCall) and ir.function in require_functions:
                #print(ir.node)
                self.create_require(ir.node)

    def load_irs(self, _nodes: List[Slither_NodeSolc]):
        """
        Loading IRs of the function.
        Currently not used.

        Notes:
            Slither IR is always placing code within modifiers at the end of the function.
            We are only loading non

        *** To be completed.
            ❌We may not need this after all.....
        """
        for n in _nodes:
            if not n.irs:
                continue

            for ir in n.irs:
                if isinstance(ir, Slither_InternalCall):
                    if isinstance(ir, Slither_FunctionSolc):
                        self.load_irs_helper(ir.function.nodes)
                else:
                    self.ir_list.append(ir)

    def create_require(self, _require: Slither_NodeSolc):
        """
        Creating require objects.

        *** To be completed.
            ❌There could be duplicate state or local variables added to the function.
                ✔There shouldn't be any duplicate state variables since they are only created once, and they are added to a set.
                There might be duplicate local variables.
            Because all state and local variables from modifier objects have already been loaded using load_modifiers().
            Take a look into this and confirm.
        """
        self.load_state_variables(_require.state_variables_read, 'read')
        self.load_local_variables(_require.variables_read, 'read')
        new_require = Require(_require, self)

        self.requires.add(new_require)

        """
        This seems to be duplicate code as the above. 
        Investigate. 
        """
        for state_variable in new_require.state_variables_read:
            if state_variable not in self.state_variables_read:
                self.state_variables_read.add(state_variable)

    def load_modifiers(self, _function: Slither_Function):
        """
        Loading modifier objects.

        Finished.
        """
        for modifier in _function.modifiers:
            # adding modifier objects to current function.
            self.modifiers.add(self.from_contract.modifiers[modifier.name])

            # adding state variables written from modifier to current function.
            for state_variable in self.from_contract.modifiers[modifier.name].state_variables_written:
                self.state_variables_written.add(state_variable)

            # adding state variables read from modifier to current function.
            for state_variable in self.from_contract.modifiers[modifier.name].state_variables_read:
                self.state_variables_read.add(state_variable)

            # loading requires from modifiers into current function.
            self.load_modifier_requires(modifier)

    def __str__(self):
        """
        Overrides str.

        Finished.
        """
        return self.signature

    def __repr__(self):
        """
        Overrides print.

        Finished.
        """
        return self.signature

    def function_summary(self):
        """
        For returning the summary of the function.

        Finished.
        """
        res = []
        res.append(f'Function: {self.signature}')
        res.append(f'\tVisibility: {self.visibility}')

        res.append(f'\tModifiers: ')
        for m in self.modifiers:
            res.append(f'\t\t{str(m)}')

        res.append(f'\tRequires:')
        for r in self.requires:
            res.append(f'\t\t{str(r)}')

        v = ''
        for s in self.state_variables_read:
            v += s.name + ', '
        res.append(f'\tState Vars Read: {v[:-2]}')

        v = ''
        for s in self.state_variables_written:
            v += s.name + ', '
        res.append(f'\tState Vars Written: {v[:-2]}')

        v = ''
        for s in self.local_variables_read:
            v += s.name + ', '
        res.append(f'\tLocal Vars Read: {v[:-2]}')

        v = ''
        for s in self.local_variables_written:
            v += s.name + ', '
        res.append(f'\tLocal Vars Written: {v[:-2]}')

        return '\n'.join(res)





# static utility functions


