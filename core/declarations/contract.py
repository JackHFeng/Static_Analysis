from web3 import Web3
from solc import compile_standard

from slither.core.declarations.contract import Contract as Slither_Contract
from slither.core.declarations.function import Function as Slither_Function
from slither.core.declarations.modifier import Modifier as Slither_Modifier

from .function import Function
from .modifier import Modifier
from .state_variable import StateVariable
from .opcode import Opcode


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

        # deployed opcode
        self._opcodes_str = None

        self._opcodes = {}

        # source code
        self._code = None

        # set of edges in tuples
        self._edges = set()

        # source directory
        self._source_dir = None  # set in ctfuzz

        # currently not used, this is for storing contract address after deployment
        # self._address = None

        self._setter(contract)

    @property
    def name(self):
        return self._name

    @property
    def functions(self):
        return self._functions.values()

    @property
    def total_functions(self):
        return len(self._functions)

    @property
    def functions_dic(self):
        return self._functions

    @property
    def state_variables(self):
        return self._state_variables.values()

    @property
    def state_variables_dic(self):
        return self._state_variables

    @property
    def modifiers(self):
        return self._modifiers.values()

    @property
    def modifiers_dic(self):
        return self._modifiers

    @property
    def default_satisfied_functions(self):
        return list(self._default_satisfied_functions)

    @property
    def abi(self):
        return self._abi

    def set_abi(self, abi):
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

    def set_bin_code(self, bin_code):
        self._bin_code = bin_code.strip()

    @property
    def opcodes_str(self):
        return self._opcodes_str

    """
    Probably need another property to provide some customized opcode info
    """

    def set_opcodes_str(self, opcodes_str):
        self._opcodes_str = opcodes_str.strip()

    @property
    def opcodes_dic(self):
        return self._opcodes

    def set_opcodes_dic(self, opcodes_dic):
        self._opcodes = opcodes_dic

    @property
    def code(self):
        return self._code

    def set_code(self, code):
        self._code = code

    @property
    def edges(self):
        return list(self._edges)

    @property
    def total_edges(self):
        """
        It would be
            return len(self._edges)
        if we actually know the edges.

        But this will work.
        """
        opcodes_list = self._opcodes_strsplit(' ')

        count_JD_sequence = 0  # sequence where pc enters JUMPDEST from non JUMP opcode.
        for i in range(len(opcodes_list)):
            if opcodes_list[i] != "JUMPDEST":
                continue
            else:
                if opcodes_list[i - 1] not in ['JUMP', 'JUMPI', 'STOP', 'RETURN', 'REVERT']:
                    count_JD_sequence += 1
        return self._opcodes.count("JUMPI ") * 2 + self._count("JUMP ") + count_JD_sequence

    def set_edges(self, edges):
        self._edges = edges

    @property
    def source_dir(self):
        return self._source_dir

    def set_source_dir(self, source_dir):
        self._source_dir = source_dir

    def add_default_sat_function(self, function):
        self._default_satisfied_functions.add(function)

    def _setter(self, contract: Slither_Contract):
        self._name = contract.name

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

    def get_function_by_name(self, name: str) -> Function:
        """
        Getter function for getting a function object
        using its name, if function does not exist
        None will be returned.

        Finished.
        """
        return self._functions.get(name)

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

    def _create_function(self, function: Slither_Function):
        """
        Creates a function object, then adds to the map.

        Finished.
        """
        new_function = Function(function, self)

        self._functions[new_function.canonical_name] = new_function

    def _create_modifier(self, modifier: Slither_Modifier):
        """
        Creates a modifier object, then adds to the map.

        Finished.
        """
        new_modifier = Modifier(modifier, self)

        self._modifiers[new_modifier.canonical_name] = new_modifier

    def __str__(self):
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
        from .utils import increase_indentation

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

        for f in self._functions.values():
            res.append(increase_indentation(f.summary))
            res.append('')

        return '\n'.join(res)

    def load_compiled_info(self):
        self.set_code(open(self._source_dir, 'r', encoding='utf-8').read())
        compiled_sol = self._compile_source()

        self.set_abi(compiled_sol['abi'])
        self.set_bin_code(compiled_sol['evm']['bytecode']['object'])
        self.set_opcodes_str(compiled_sol['evm']['deployedBytecode']['opcodes'])
        self.set_opcodes_dic(self._create_opcodes_dic())
        self._set_function_hashes()

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
                    "content": self.code
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
        from ....vandal.bin.generate_cfg import vandal_cfg
        res = vandal_cfg(self.runtime_bin_code).strip().split('\n')

        blocks = {}
        temp_block = None

        i = 0

        while i < len(res):
            if res[i].startswith('Block'):
                temp_block = Block()
                pc = int(res[i].strip().split(' ')[1], 0)
                temp_block.pc = pc
                temp_block.start = pc
            elif res[i].startswith('Predecessors'):
                p_list = res[i][15:-1].split(', ')
                for p in p_list:
                    if p:
                        temp_block.pre.append(int(p, 0))
            elif res[i].startswith("Successors"):
                p_list = res[i][13:-1].split(', ')
                for p in p_list:
                    if p:
                        temp_block.next.append(int(p, 0))
                i += 1

                while not res[i + 1].startswith('---'):
                    i += 1

                temp_block.end = int(res[i].strip().split(' ')[0], 0)

                blocks[temp_block.pc] = temp_block

            i += 1
        self._set_blocks_dic(blocks)

