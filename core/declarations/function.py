from typing import List

from slither.core.declarations.function import Function as Slither_Function
from slither.solc_parsing.declarations.modifier import ModifierSolc
from slither.slithir.operations.internal_call import InternalCall as Slither_InternalCall
from slither.solc_parsing.cfg.node import NodeSolc as Slither_NodeSolc
from slither.solc_parsing.declarations.function import FunctionSolc as Slither_FunctionSolc

from .function_call import FunctionCall


# types of require function calls for getting the list of requires.


class Function(FunctionCall):
    """
    still need to handle for ctfuzz
        para_names, "a, b, c"
        str_tc, string format of the tc
        next_tc, index for next test case
        new_ipm, flag for check if new ipm happened.
    """
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

        self._is_constructor = None

        # set of modifiers.
        self._modifiers = set()

        # list of IRs
        # we may not need this after all.
        self._irs = []

        # whether the function is view type
        # will not alter the storage
        self._view = None

        # whether the function is pure type
        # on top of view will not even access storage
        self._pure = None

        # whether a function can receive ether
        self._payable = None

        # whether the current function can be satisfied by default / right after deployment
        self._sat_by_default = False

        # hash of the function/modifier signature
        self._sig_hash = None

        # CT test cases, to be fuzzed.
        self._test_cases = []

        # for storing test cases that has been fuzzed.
        self._fuzzed_test_cases = []

        self._acts_tc_str = None

        self._w3_function = None

        self._z3 = None

        self._z3_requires = {}

        # if ever entered without revert
        self._entered = False

        self._opcodes = {}

        self._covered_opcodes = set()

        self._blocks = {}

        self._edges = set()

        self._covered_edges = set()

        self._opcode_start_pc = float('inf')

        self._opcode_end_pc = float('-inf')

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
    def is_constructor(self):
        return self._is_constructor

    @property
    def modifiers(self):
        return self._modifiers

    @property
    def irs(self):
        return self._irs

    @property
    def view(self):
        return self._view

    @property
    def pure(self):
        return self._pure

    @property
    def payable(self):
        return self._payable

    @property
    def sat_by_default(self):
        return self._sat_by_default

    @property
    def sig_hash(self):
        return self._sig_hash

    def load_sig_hash(self, sig_hash):
        self._sig_hash = sig_hash

    @property
    def test_cases(self):
        test_cases = []
        for tc in self._test_cases:
            concrete_tc = {}
            for k, v in tc.items():
                concrete_tc[k] = self.get_parameter_by_name(k).get_w3_rep_value(v)
            test_cases.append(concrete_tc)
        return test_cases

    @property
    def raw_test_cases(self):
        return self._test_cases

    @property
    def total_test_cases(self):
        return len(self._test_cases)

    def clear_test_cases(self):
        self._test_cases = []

    @property
    def fuzzed_test_cases(self):
        return self._fuzzed_test_cases

    def add_fuzzed_test_case(self, tc):
        self._fuzzed_test_cases.append(tc)

    @property
    def total_fuzzed_test_cases(self):
        return len(self._fuzzed_test_cases)

    @property
    def acts_tc_str(self):
        return self._acts_tc_str

    def set_acts_str(self, tc):
        self._acts_tc_str = tc

    @property
    def w3_function(self):
        return self._w3_function

    def load_w3_function(self, w3_function):
        self._w3_function = w3_function

    @property
    def z3(self):
        return self._z3

    def set_z3(self, obj):
        self._z3 = obj

    @property
    def z3_requires(self):
        return self._z3_requires

    def add_z3_require(self, key, obj):
        self._z3_requires[key] = obj

    def load_test_cases(self, tcs):
        self._test_cases = tcs

    @property
    def entered(self):
        return self._entered

    def set_entered(self):
        self._entered = True

    @property
    def opcodes(self):
        return list(self._opcodes.values())

    @property
    def total_opcodes(self):
        return len(self._opcodes.keys())

    @property
    def opcodes_dic(self):
        return self._opcodes

    def add_opcode(self, opcode):
        self._opcodes[opcode.pc] = opcode

    @property
    def covered_opcodes(self):
        return self._covered_opcodes

    def add_covered_opcode(self, pc):
        self._covered_opcodes.add(self.opcodes_dic[pc])

    @property
    def total_covered_opcodes(self):
        return len(self.covered_opcodes)

    @property
    def opcode_code_coverage(self):
        if self.total_covered_opcodes == 0 or self.total_opcodes == 0:
            return '%.2f' % 0
        return '%.2f' % round(self.total_covered_opcodes / self.total_opcodes * 100, 2)

    @property
    def opcode_code_coverage_str(self):
        return f'{self.opcode_code_coverage}% ({self.total_covered_opcodes}/{self.total_opcodes})'

    @property
    def blocks(self):
        return list(self._blocks.values())

    @property
    def blocks_dic(self):
        return self._blocks

    def add_block(self, block):
        self._blocks[block.pc] = block

    @property
    def total_blocks(self):
        return len(self._blocks)

    @property
    def edges(self):
        return list(self._edges)

    @property
    def total_edges(self):
        return len(self._edges)

    def add_edge(self, edge):
        self._edges.add(edge)
        # nl = '\r\n'
        # print(f'{edge[0].original_function.full_name} [{edge[0].block.start.pc}  {edge[0].pc}][{edge[0].source_code.split(nl)[0]}] => [{edge[1].pc}  {edge[1].block.end.pc}][{edge[1].source_code.split(nl)[0]}]')

    @property
    def covered_edges(self):
        return self._covered_edges

    @property
    def total_covered_edges(self):
        return len(self._covered_edges)

    def add_covered_edge(self, edge):
        self._covered_edges.add(edge)

    @property
    def total_uncovered_edges(self):
        return self.total_edges - self.total_covered_edges

    @property
    def edge_coverage(self):
        if self.total_covered_edges == 0 and self.total_edges == 0:
            return '%.2f' % round(0)
        return '%.2f' % round(self.total_covered_edges / self.total_edges * 100, 2)

    @property
    def edge_coverage_str(self):
        return f'{self.edge_coverage}% ({self.total_covered_edges}/{self.total_edges})'

    @property
    def opcode_start_pc(self):
        return self._opcode_start_pc

    def set_opcode_start(self, pc):
        self._opcode_start_pc = pc

    @property
    def opcode_end_pc(self):
        return self._opcode_end_pc

    def set_opcode_end(self, pc):
        self._opcode_end_pc = pc

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

    @property
    def summary(self):
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
        for s in self.parameters:
            v += s.name + ', '
        res.append(f'\tParameters: {v[:-2]}')

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

        res.append(f'\tSatisfied by Default: {self._sat_by_default}')

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
        self._full_name = function.full_name
        self._canonical_name = function.canonical_name
        self._signature = function.signature_str
        self._visibility = function.visibility
        self._parent_contract = parent_contract
        self._declared_by = function.contract_declarer.name
        self._view = True if function.view else False
        self._pure = True if function.pure else False
        self._payable = True if function.payable else False
        self._is_constructor = True if function.is_constructor else False
        self._slither_function = function

        # load parameters.
        # this step must happen first, because parameters are added to both the parameter and local variable list.
        self._load_parameters(function)

        # load both written local and state variables.
        self._load_variables(function)

        # we may not need this after all.
        # self.load_irs(_function.nodes)

        # load modifier objects.
        # requires within modifiers will be loaded into self.requires as well.
        self._load_modifiers(function)

        # load requires at the front of the function.
        self._load_requires(function)

        # check if current function can be satisfied by default/ right after deployment
        self._check_sat_by_default()

    def _check_sat_by_default(self):
        for require in self._requires:
            if require.sat_cond_class != 1:
                return
        self._sat_by_default = True
        self._parent_contract.add_default_sat_function(self)

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
        from .solidity_variable import SolidityVariable
        from .solidity_variable_composed import SolidityVariableComposed
        import copy
        """
        Loading modifier objects.

        Finished.
        """
        for modifier in function.modifiers:
            if not isinstance(modifier, ModifierSolc):
                continue
            # getting the modifier object
            modifier_object = self._parent_contract.modifiers_dic[modifier.canonical_name]

            # adding modifier object to current function.
            self._modifiers.add(modifier_object)

            # adding state variables written from modifier to current function.
            for state_variable in modifier_object.state_variables_written:
                self._state_variables_written.add(state_variable)

            # adding state variables read from modifier to current function.
            for state_variable in modifier_object.state_variables_read:
                self._state_variables_read.add(state_variable)

            for local_variable in modifier_object.local_variables_read:
                if (
                        type(local_variable) in [SolidityVariable, SolidityVariableComposed] and
                        local_variable.name not in [p.name for p in self.parameters]
                ):
                    new_parameter = copy.deepcopy(local_variable)
                    new_parameter._rep_values = []
                    self.add_parameter(new_parameter)
                    self.add_local_variable(new_parameter)
                    self._local_variables_read.add(new_parameter)

            # adding requires from modifier into current function.
            for require in modifier_object.requires:
                self._requires.add(require)


    # end of region
    ###################################################################################
    ###################################################################################
    # region => private functions
    ###################################################################################
    ###################################################################################
