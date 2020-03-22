from web3 import Web3
from solc import compile_standard

from slither.core.declarations.contract import Contract as Slither_Contract
from slither.core.declarations.function import Function as Slither_Function
from slither.core.declarations.modifier import Modifier as Slither_Modifier

from .function import Function
from .modifier import Modifier
from .state_variable import StateVariable
from .opcode import Opcode
from .block import Block

from termcolor import colored


def increase_indentation(s: str):
    """
    For the purpose of generating summaries.
    """
    return '\t' + '\t'.join(s.splitlines(True))


def set_function_edges(left, right):
    if left.original_function == right.original_function \
            and left.original_function:
        left.original_function.add_edge((left, right))


class Contract:
    """
    Contract object.

    *** To be completed.
    """

    def __init__(self, contract: Slither_Contract):
        """
        *** To be completed.
            default_satisfied_functions attribute is still yet to be loaded.

        *** to be handled for ctfuzz
            new_ipm, flag for whether theres new ipm for any of the functions in this contract.
        """

        # e.g. "Ballot".
        self._name = None

        # map of functions with their name as key.
        self._functions = {}

        # list of constructors
        self._constructor = None

        # map of state variables with their name as key.
        self._state_variables = {}

        # map of modifiers with their name as key.
        self._modifiers = {}

        # functions that can be executed right after contract deployment,
        # because their requires can be satisfied at the Initial state.
        self._default_satisfied_functions = set()

        # abi of current contract
        self._abi = None

        # contract binary
        self._bin_code = None

        # runtime binary after deployment
        self._runtime_bin_code = None

        # deployed opcode
        self._opcodes_str = None

        # source map of deployed opcode
        self._source_map_str = None

        # opcode objects. With pc as key
        self._opcodes = {}

        self._covered_opcodes = set()

        # basic blocks for cfg. With entry pc as key.
        # start, end, pre, next are stored with opcode objects.
        self._blocks = {}

        # source code
        self._source_code = None

        # source code in bytes
        self._source_code_bytes = None

        # set of edges in tuples with pc number
        self._edges = set()

        self._covered_edges = set()

        # source directory
        self._source_dir = None  # set in ctfuzz

        # currently not used, this is for storing contract address after deployment
        # self._address = None

        self._w3_contract = None

        self._slither_contract = None

        self._setter(contract)

    @property
    def name(self):
        return self._name

    @property
    def functions(self):
        return list(self._functions.values())

    @property
    def total_functions(self):
        return len(self._functions)

    @property
    def functions_dic(self):
        return self._functions

    @property
    def constructor(self):
        return self._constructor

    @property
    def state_variables(self):
        return list(self._state_variables.values())

    @property
    def state_variables_dic(self):
        return self._state_variables

    @property
    def modifiers(self):
        return list(self._modifiers.values())

    @property
    def modifiers_dic(self):
        return self._modifiers

    @property
    def default_satisfied_functions(self):
        return list(self._default_satisfied_functions)

    @property
    def abi(self):
        return self._abi

    def _set_abi(self, abi):
        """
        This abi is still in json format, which means it contains nested lists and dictionaries.
        Args:
            abi:

        Returns:

        """
        self._abi = abi

    @property
    def bin_code(self):
        return self._bin_code

    def _set_bin_code(self, bin_code):
        self._bin_code = bin_code.strip()

    @property
    def runtime_bin_code(self):
        return self._runtime_bin_code

    def _set_runtime_bin_code(self, runtime_bin_code):
        self._runtime_bin_code = runtime_bin_code.strip()

    @property
    def opcodes_str(self):
        return self._opcodes_str

    """
    Probably need another property to provide some customized opcode info
    """

    def _set_opcodes_str(self, opcodes_str):
        self._opcodes_str = opcodes_str.strip()

    @property
    def source_map_str(self):
        return self._source_map_str

    def _set_source_map_str(self, source_map_str):
        self._source_map_str = source_map_str

    @property
    def opcodes(self):
        return list(self._opcodes.values())

    @property
    def total_opcodes(self):
        return len(self._opcodes.keys())

    @property
    def opcodes_dic(self):
        return self._opcodes

    def _set_opcodes_dic(self, opcodes_dic):
        self._opcodes = opcodes_dic

    @property
    def covered_opcodes(self):
        return self._covered_opcodes

    def add_covered_opcode(self, pc):
        opcode = self.opcodes_dic[pc]
        self._covered_opcodes.add(opcode)

        if opcode.original_function:
            opcode.original_function.add_covered_opcode(pc)

    @property
    def total_covered_opcodes(self):
        return len(self.covered_opcodes)

    @property
    def opcode_code_coverage(self):
        return '%.2f' % round(self.total_covered_opcodes / self.total_opcodes * 100, 2)

    @property
    def opcode_code_coverage_str_colored(self):
        return f'Contract Opcode Coverage: {colored(self.opcode_code_coverage, "cyan", "on_green", attrs=["bold"])}% ' \
               f'({self.total_covered_opcodes}/{self.total_opcodes})'

    @property
    def opcode_code_coverage_str(self):
        return f'Contract Opcode Coverage: {self.opcode_code_coverage}% ({self.total_covered_opcodes}/' \
               f'{self.total_opcodes})'

    @property
    def blocks(self):
        return list(self._blocks.values())

    @property
    def blocks_dic(self):
        return self._blocks

    def _set_blocks_dic(self, blocks_dic):
        self._blocks = blocks_dic
        for block in blocks_dic.values():
            if block.start.original_function == block.end.original_function \
                    and block.start.original_function:
                block.start.original_function.add_block(block)

    @property
    def total_blocks(self):
        return len(self._blocks)

    @property
    def source_code(self):
        return self._source_code

    @property
    def source_code_bytes(self):
        return self._source_code_bytes

    def _set_source_code(self, source_code):
        self._source_code = source_code

    def _set_source_code_bytes(self, source_code_bytes):
        self._source_code_bytes = source_code_bytes

    @property
    def edges(self):
        return list(self._edges)

    @property
    def total_edges(self):
        return len(self._edges)

    def _set_edges(self):
        for block in self.blocks:
            left = block.end
            for successor in block.next:
                right = successor
                self._edges.add((left, right))
                set_function_edges(left, right)

    def add_missing_edge(self, edge):
        edge[0].block.next.append(edge[1])
        edge[1].block.pre.append(edge[0])

        self._edges.add(edge)
        if edge[0].original_function == edge[1].original_function \
                and edge[0].original_function:
            edge[0].original_function.add_edge(edge)

    @property
    def covered_edges(self):
        return self._covered_edges

    @property
    def total_covered_edges(self):
        return len(self._covered_edges)

    def add_covered_edge(self, edge):
        if edge in self._covered_edges:
            return False
        else:
            self._covered_edges.add(edge)
            if edge[0].original_function == edge[1].original_function \
                    and edge[0].original_function:
                edge[0].original_function.add_covered_edge(edge)
            return True

    @property
    def total_uncovered_edges(self):
        return self.total_edges - self.total_covered_edges

    @property
    def edge_coverage(self):
        return '%.2f' % round(self.total_covered_edges / self.total_edges * 100, 2)

    @property
    def edge_coverage_str_colored(self):
        return f'Contract Edge Coverage: {colored(self.edge_coverage, "cyan", "on_green", attrs=["bold"])}% ' \
               f'({self.total_covered_edges}/{self.total_edges})'

    @property
    def edge_coverage_str(self):
        return f'Contract Edge Coverage: {self.edge_coverage}% ({self.total_covered_edges}/{self.total_edges})'

    @property
    def functions_coverage_colored(self):
        res = []
        for function in self.functions:
            if function.name not in ['slitherConstructorVariables', 'slitherConstructorConstantVariables']:
                res.append(f'{colored(function.full_name, "cyan", "on_green", attrs=["bold"])} edge_cov: '
                           f'{colored(function.edge_coverage_str, "cyan", "on_green", attrs=["bold"])}  opcode_cov: '
                           f'{colored(function.opcode_code_coverage_str, "cyan", "on_green", attrs=["bold"])}')
        return '\n'.join(res)

    @property
    def functions_coverage(self):
        res = []
        for function in self.functions:
            if function.name not in ['slitherConstructorVariables', 'slitherConstructorConstantVariables']:
                res.append(f'{function.full_name} edge_cov: {function.edge_coverage_str} opcode_cov:'
                           f' {function.opcode_code_coverage_str}')

        return '\n'.join(res)

        return '\n'.join(res)

    @property
    def source_dir(self):
        return self._source_dir

    @property
    def w3_contract(self):
        return self._w3_contract

    @property
    def slither_contract(self):
        return self._slither_contract

    def load_w3_contract(self, w3_contract):
        self._w3_contract = w3_contract

    def load_source_dir(self, source_dir):
        self._source_dir = source_dir

    def add_default_sat_function(self, function):
        self._default_satisfied_functions.add(function)

    def _setter(self, contract: Slither_Contract):
        self._name = contract.name
        self._slither_contract = contract

        self._create_constructor(contract)

        # create modifier objects.
        for modifier in contract.modifiers:
            self._create_modifier(modifier)

        # create function objects.
        """
        ***Only newer versions of slither have this
        Slither has a inbuilt function called 
            FunctionType.CONSTRUCTOR_VARIABLES: "slitherConstructorVariables". 
            FunctionType.CONSTRUCTOR_CONSTANT_VARIABLES: "slitherConstructorConstantVariables"
        These are dummy function that holds the state variable declaration statements. 
        Constant are for constant state variables. 
        E.g. uint a = 0;
             uint constant a = 0;

        However, if a state variable is only declared without value assignment, 
        it will not show up in the dummy function. 
        E.g. uint a;
        """
        for function in contract.functions:
            self._create_function(function)

    def get_function_by_name(self, name):
        """
        ****Deprecated
        Getter function for getting a function object
        using its name, if function does not exist
        None will be returned.

        Finished.
        """
        for f in self.functions:
            if f.name == name:
                return f

    def get_function_by_full_name(self, name):
        for f in self.functions:
            if f.full_name == name:
                return f

    def get_function_by_source_map(self, offset, length):
        for function in self.functions:
            if function.name in ['slitherConstructorVariables', 'slitherConstructorConstantVariables']:
                continue
            f_start = function.slither_function.source_mapping['start']
            f_length = function.slither_function.source_mapping['length']
            f_end = f_start + f_length
            end = offset + length
            if f_start <= offset \
                    and f_end >= end:
                return function

    def get_function_by_sig_hash(self, sig_hash: str) -> Function:
        for f in self.functions:
            if f.sig_hash == sig_hash:
                return f

    def get_modifier_by_name(self, name: str) -> Modifier:
        """
        Getter function for getting a modifier object
        using its name, if modifier does not exist
        None will be returned.

        Finished.
        """
        return self._modifiers.get(name)

    def get_state_variable_by_name(self, name: str) -> StateVariable:
        """
        Getter function for getting a state variable object
        using its name, if state variable does not exist
        None will be returned.

        Finished.
        """
        return self._state_variables.get(name)

    def _create_constructor(self, contract: Slither_Contract):
        # if contract has no constructor at all, return
        if not contract.constructors:
            return
        # the constructor of current function
        temp_constructor = None
        if contract.constructor:
            # has its own constructor
            temp_constructor = contract.constructor
            self._constructor = Function(temp_constructor, self)
        else:
            from .local_variable import LocalVariable
            # does not have own, but have others, just pick the first one.
            temp_constructor = contract.constructors[0]
            self._constructor = Function(temp_constructor, self)
            for k, v, in self._constructor.parameters:
                if type(v) == LocalVariable:
                    del self._constructor._parameters[k]

        for constructor in contract.constructors:
            # load sol_vars read by other constructors
            if constructor != temp_constructor:
                for sol_var in constructor.solidity_variables_read:
                    self._constructor.load_local_variables_helper(sol_var, 'read')

    def _create_function(self, function: Slither_Function):
        """
        Creates a function object, then adds to the map.

        Finished.
        """
        new_function = Function(function, self)
        if new_function.is_constructor:
            self._constructors.append(new_function)
        else:
            self._functions[new_function.canonical_name] = new_function

        # create function objects for library functions.
        if function.library_calls:
            for function_tuple in function.library_calls:
                self._create_function(function_tuple[1])

    def _create_modifier(self, modifier: Slither_Modifier):
        """
        Creates a modifier object, then adds to the map.

        Finished.
        """
        new_modifier = Modifier(modifier, self)

        self._modifiers[new_modifier.canonical_name] = new_modifier

        if modifier.library_calls:
            for function_tuple in modifier.library_calls:
                self._create_function(function_tuple[1])

    def __str__(self):
        """
        Returns contract name.

        Finished
        """
        return self._name

    def __repr__(self):
        """
        Returns contract name.

        Finished
        """
        return self._name

    @property
    def summary(self):
        """
        Prints the summary of the contract.

        Finished.
        """

        res = list()
        res.append(f'Contract Name: {self._name}')

        res.append(f'State Variables: ')
        for v in self._state_variables.values():
            res.append(f'\t{v.name}({v.type}): {v.default_value}')
            res.append(f'\t\tinitialized: {v.initialized}')
            res.append(f'\t\tinitialized by constructor: {v.set_by_constructor}')
            res.append(f'\t\tinitialized by SolcVar: {v.set_by_deployment}')
            if v.set_by_deployment:
                res.append(f'\t\t\tusing: {v.var_used_in_deployment}')
            res.append('')
        res.append('')

        res.append(f'Modifiers: ')

        for m in self._modifiers.values():
            res.append(increase_indentation(m.summary))
            res.append('')

        res.append(f'Functions: ')

        for f in [self.constructor] + self.functions:
            res.append(increase_indentation(f.summary))
            res.append('')

        return '\n'.join(res)

    def list_requires(self):
        res = [self.name]
        for f in [self.constructor] + self.functions:
            for r in f.requires:
                res.append(f'\t{str(r)}')
        return '\n'.join(res)

    def load_compiled_info(self):
        # these source codes are for source mapping
        self._set_source_code_bytes(open(self._source_dir, 'rb').read())
        self._set_source_code(self.source_code_bytes.decode('utf-8'))
        compiled_sol = self._compile_source()

        self._set_abi(compiled_sol['abi'])
        self._set_bin_code(compiled_sol['evm']['bytecode']['object'])
        self._set_runtime_bin_code(compiled_sol['evm']['deployedBytecode']['object'])
        self._set_opcodes_str(compiled_sol['evm']['deployedBytecode']['opcodes'])
        self._set_source_map_str(compiled_sol['evm']['deployedBytecode']['sourceMap'])
        self._set_opcodes_dic(self._create_opcodes_dic())

        self._create_mapping()

        self._set_blocks()
        self._set_edges()
        self._set_function_hashes()

    def load_w3_functions(self):
        from util import is_fuzzing_candidate
        for function in self.functions:
            if is_fuzzing_candidate(function):
                if function.name == 'fallback':
                    w3_function = self.w3_contract.fallback
                else:
                    w3_function = self.w3_contract.get_function_by_selector(function.sig_hash)
                function.load_w3_function(w3_function)

    def _compile_source(self):
        """
        Finished.
        Compiles the source solidity code and returns the
            binary, abi, runtime opcode in a dictionary format.
        Returns:
            dictionary containing the above info.
        """
        filename = self.source_dir.split('/')[-1]
        compiled_sol = compile_standard({
            "language": "Solidity",
            "sources": {
                filename: {
                    "content": self.source_code
                }
            },
            "settings":
                {
                    "outputSelection": {
                        "*": {
                            "*": [
                                "abi", "evm.bytecode", "evm.deployedBytecode"
                            ]
                        }
                    }
                }
        })
        return compiled_sol['contracts'][filename][self.name]

    def _create_opcodes_dic(self):
        """
        Finished.
        This creates the dictionary for the opcodes.
        The key is the pc, the value is the opcode node.
        The opcodes are connected as doubly linked list,
        So we can find it's previous and next node.
        Due to the pc are not continuous when PUSH* happens.
        Returns:
            opcode dictionary

        """
        opcodes_dic = {}

        # split the string opcodes, which also separated PUSH* and their value
        temp_list = self.opcodes_str.split(' ')
        op_list = []

        # connecting push with their value, and adding them to the op_list
        # then we have our opcodes in the correct order. Without pc.
        for line in temp_list:
            if line.startswith("0x") and op_list[-1].startswith('PUSH') and '0x' not in op_list[-1]:
                # this if also handles invalid opcodes that did not appear after PUSH*
                op_list[-1] += f' {line}'
            else:
                op_list.append(line)

        # creating the dic with opcode nodes and compute their correct pc number.
        # dummy head
        head = Opcode()
        head.pc = -1
        head.size = 0
        import re

        for line in op_list:
            node = Opcode()
            temp_list = line.split(' ')  # this gives the PUSH* and their value if its a PUSH*
            node.opcode = temp_list[0]  # sets the opcode
            node.value = temp_list[1] if len(temp_list) > 1 else None  # sets the value if there is any
            node.size = int(re.sub(r'\D', '', node.opcode)) if node.value else 0  # sets the value if there is any

            node.pc = head.pc + head.size + 1
            node.pre = head
            head.next = node
            head = node
            opcodes_dic[head.pc] = head

        opcodes_dic[0].pre = None
        return opcodes_dic

    def _create_mapping(self):
        def parse_source_map(source_map_str):
            import copy

            res = []
            maps = source_map_str.split(';')
            temp = [0, 0, 0, '']
            for m in maps:
                map_list = copy.deepcopy(temp)
                elements = m.split(':')
                for i in range(len(elements)):
                    element = elements[i]
                    if element:
                        if i == 3:
                            temp[i] = element
                            map_list[i] = element
                        else:
                            temp[i] = int(element)
                            map_list[i] = int(element)
                    else:
                        pass
                res.append(map_list)
            return res

        mapping_list = parse_source_map(self.source_map_str)
        opcode = self.opcodes_dic[0]

        index_tracker = {}
        # needs to be poped out at the end.
        while mapping_list:

            # check if source index is -1, mean no valid map.
            if mapping_list[0][2] == -1:
                # print(f'{opcode} => {mapping_list[0]}')
                opcode.source_map = mapping_list[0]
                mapping_list.pop(0)
                opcode = opcode.next
                continue

            offset = mapping_list[0][0]
            length = mapping_list[0][1]
            original_function = self.get_function_by_source_map(offset, length)

            if not original_function:
                opcode.source_map = mapping_list[0]
                mapping_list.pop(0)
                opcode = opcode.next
                continue

            # handle fallback function
            if original_function.full_name == 'fallback()':
                # first opcode of fallback function
                if not index_tracker.get('fallback()'):
                    index_tracker['fallback()'] = [opcode.pc - 1, opcode.pc]
                else:
                    index_tracker['fallback()'][1] = opcode.pc + 1
            elif original_function.visibility in ['public', 'external']:
                if not index_tracker.get(original_function.full_name):
                    if opcode.opcode == 'JUMP':
                        index_tracker[original_function.full_name] = [int(opcode.pre.value, 16),
                                                                      int(opcode.pre.value, 16)]
                else:
                    index_tracker[original_function.full_name][1] = opcode.pc
            elif original_function.visibility in ['internal', 'private']:
                if not index_tracker.get(original_function.full_name):
                    index_tracker[original_function.full_name] = [opcode.pc, opcode.pc]
                else:
                    index_tracker[original_function.full_name][1] = opcode.pc
            else:
                raise Exception(f'Unhandled case in opcode segment identification. => {opcode} {mapping_list[0]}')

            opcode.source_map = mapping_list[0]
            mapping_list.pop(0)
            opcode = opcode.next

        for k, v in index_tracker.items():
            function_obj = self.get_function_by_full_name(k)
            start = v[0]
            end = v[1]
            function_obj.set_opcode_start(start)
            function_obj.set_opcode_end(end)
            opcode = self.opcodes_dic[start]
            while opcode.pc <= end:
                if opcode.source_map[2] != -1:
                    opcode.set_original_function(function_obj)
                opcode = opcode.next

        # # needs to be poped out at the end.
        # while mapping_list:
        #     # check if source index is -1, mean no valid map.
        #     if mapping_list[0][2] == -1:
        #         print(f'{opcode} => {mapping_list[0]}')
        #         mapping_list.pop(0)
        #         opcode = opcode.next
        #         continue
        #     offset = mapping_list[0][0]
        #     length = mapping_list[0][1]
        #
        #     original_code = self.source_code_bytes[offset: offset + length].decode('utf-8')
        #     original_function = self.get_function_by_source_map(offset, length)
        #     if original_function:
        #         opcode.set_original_function(original_function, offset, length, original_code)
        #         nl = '\r\n'
        #         print(f'{opcode} => {mapping_list[0]} => {opcode.source_code.split(nl)[0]} *** '
        #               f'{opcode.original_function.name} {opcode.original_function.opcode_start_pc}
        #               {opcode.original_function.opcode_end_pc}')
        #     else:
        #         opcode.source_map = (offset, length)
        #         opcode.source_code = original_code
        #         nl = '\r\n'
        #         print(f'{opcode} => {mapping_list[0]} => {opcode.source_code.split(nl)[0]}')
        #     mapping_list.pop(0)
        #     opcode = opcode.next

    def _set_function_hashes(self):
        """
        Compute the sig hash from their full name/signature.
        Then set it for each function.

        We still need to handle the dummy functions created in slither.
        Refer back to slither about
            slitherConstructorVariables
            slitherConstructorConstantVariables

        Returns:
            None, but sets the hash for all the functions in the contract.
        """
        for f in self.functions:
            f_hash = Web3.sha3(text=f.full_name).hex()[:10]
            f.load_sig_hash(f_hash)

    def _set_blocks(self):
        from ..vandal.bin.generate_cfg import vandal_cfg
        res = vandal_cfg(self.runtime_bin_code).strip().split('\n')

        blocks = {}
        temp_block = None

        i = 0

        while i < len(res):
            if res[i].startswith('Block'):
                temp_block = Block()
                pc = int(res[i].strip().split(' ')[1], 0)
                temp_block.pc = pc
                temp_block.start = self.opcodes_dic[pc]
                # adding block ref to opcode
                self.opcodes_dic[pc].block = temp_block

            elif res[i].startswith('Predecessors'):
                p_list = res[i][15:-1].split(', ')
                for p in p_list:
                    if p:
                        # int(x, 0) hex string to int
                        temp_block.pre.append(self.opcodes_dic[int(p, 0)])
            elif res[i].startswith("Successors"):
                p_list = res[i][13:-1].split(', ')
                for p in p_list:
                    if p:
                        temp_block.next.append(self.opcodes_dic[int(p, 0)])

                i += 1

                if res[i].startswith('Has unresolved jump.'):
                    i += 1

                while not res[i + 1].startswith('---'):
                    i += 1
                temp_block.end = self.opcodes_dic[int(res[i].strip().split(' ')[0], 0)]
                # adding block ref to opcode
                self.opcodes_dic[int(res[i].strip().split(' ')[0], 0)].block = temp_block
                blocks[temp_block.pc] = temp_block

            i += 1
        self._set_blocks_dic(blocks)
