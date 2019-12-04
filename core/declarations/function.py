from .function_call import FunctionCall

from typing import List

from .local_variable import LocalVariable
from .state_variable import StateVariable
from .require import Require

from slither.core.declarations.function import Function as Slither_Function
from slither.core.variables.state_variable import StateVariable as Slither_StateVariable
from slither.core.variables.local_variable import LocalVariable as Slither_LocalVariable
from slither.slithir.operations import SolidityCall as Slither_SolidityCall
from slither.solc_parsing.cfg.node import NodeSolc as Slither_NodeSolc
from slither.slithir.operations.internal_call import InternalCall as Slither_InternalCall
from slither.solc_parsing.declarations.function import FunctionSolc as Slither_FunctionSolc

# types of require function calls for getting the list of requires.



class Function(FunctionCall):
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
    def __init__(self, function: Slither_Function, parent_contract):
        super().__init__()
        # e.g. "public", "external", "internal", etc.
        self._visibility = None

        # set of modifiers.
        self._modifiers = set()

        # list of IRs
        # we may not need this after all.
        self._irs = []

        # whether the function is view type
        self._is_view = None

        # whether the function is pure type
        self._is_pure = None

        self._setter(function, parent_contract)

    ###################################################################################
    ###################################################################################
    # region => public getters
    ###################################################################################
    ###################################################################################

    @property
    def visibility(self):
        return self._visibility

    @property
    def modifiers(self):
        return self._modifiers

    @property
    def irs(self):
        return self._irs

    @property
    def is_view(self):
        return self._is_view

    @property
    def is_pure(self):
        return self._is_pure

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
        for sv in self._state_variables_read:
            for fn in sv.functions_written:
                # only returns public functions
                if fn is not self and fn not in res and fn.visibility == 'public':
                    res.append(fn)
        return res

    def get_depended_functions_by_state_variable(self, name):
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
        # validity check, if state variable is read by function at all.
        sv_exist = False

        for sv in self._state_variables_read:
            if sv.name == name:
                sv_exist = True
                for fn in sv.functions_written:
                    # only returns public functions
                    if fn is not self and fn not in res and fn.visibility == 'public':
                        res.append(fn)
                return res

        if sv_exist:
            return res
        else:
            raise Exception(f'state variable "{name}" is not read by function "{self.name}".')
        # throw exception? Or just return empty array?

    def function_summary(self):
        """
        For returning the summary of the function.

        Finished.
        """
        res = []
        res.append(f'Function: {self._signature}')
        res.append(f'\tVisibility: {self._visibility}')

        res.append(f'\tModifiers: ')
        for m in self._modifiers:
            res.append(f'\t\t{str(m)}')

        res.append(f'\tRequires:')
        for r in self._requires:
            res.append(f'\t\t{str(r)}')

        v = ''
        for s in self._state_variables_read:
            v += s.name + ', '
        res.append(f'\tState Vars Read: {v[:-2]}')

        v = ''
        for s in self._state_variables_written:
            v += s.name + ', '
        res.append(f'\tState Vars Written: {v[:-2]}')

        v = ''
        for s in self._local_variables_read:
            v += s.name + ', '
        res.append(f'\tLocal Vars Read: {v[:-2]}')

        v = ''
        for s in self._local_variables_written:
            v += s.name + ', '
        res.append(f'\tLocal Vars Written: {v[:-2]}')

        return '\n'.join(res)

    def __str__(self):
        """
        Overrides str.

        Finished.
        """
        return self._signature

    def __repr__(self):
        """
        Overrides print.

        Finished.
        """
        return self._signature

    # end of region
    ###################################################################################
    ###################################################################################
    # region => public getters
    ###################################################################################
    ###################################################################################

    ###################################################################################
    ###################################################################################
    # region => private functions
    ###################################################################################
    ###################################################################################

    def _setter(self, function: Slither_Function, parent_contract):
        """
        Setting values when initializing

        Finished.
        """
        self._name = function.name
        self._signature = function.signature_str
        self._visibility = function.visibility
        self._parent_contract = parent_contract
        self._is_view = True if function.view else False
        self._is_pure = True if function.pure else False

        # load parameters.
        self._load_parameters(function)

        # load both local and state variables.
        self._load_variables(function)

        # we may not need this after all.
        # self.load_irs(_function.nodes)

        # load modifier objects.
        # requires within modifiers will be loaded into self.requires as well.
        self._load_modifiers(function)

        # load requires at the front of the function.
        self._load_requires(function)

    def _load_irs(self, nodes: List[Slither_NodeSolc]):
        """
        Loading IRs of the function.
        Currently not used.

        Notes:
            Slither IR is always placing code within modifiers at the end of the function.
            We are only loading non

        *** To be completed.
            ❌We may not need this after all.....
        """
        for n in nodes:
            if not n.irs:
                continue

            for ir in n.irs:
                if isinstance(ir, Slither_InternalCall):
                    if isinstance(ir, Slither_FunctionSolc):
                        self.load_irs_helper(ir.function.nodes)
                else:
                    self._irs.append(ir)

    def _load_modifiers(self, function: Slither_Function):
        """
        Loading modifier objects.

        Finished.
        """
        for modifier in function.modifiers:
            # getting the modifier object
            modifier_object = self._parent_contract.modifiers[modifier.name]

            # adding modifier object to current function.
            self._modifiers.add(modifier_object)

            # adding state variables written from modifier to current function.
            for state_variable in modifier_object.state_variables_written:
                self._state_variables_written.add(state_variable)

            # adding state variables read from modifier to current function.
            for state_variable in modifier_object.state_variables_read:
                self._state_variables_read.add(state_variable)

            # adding requires from modifier into current function.
            for require in modifier_object.requires:
                self._requires.add(require)

    # end of region
    ###################################################################################
    ###################################################################################
    # region => private functions
    ###################################################################################
    ###################################################################################
