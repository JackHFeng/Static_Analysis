from collections import defaultdict
import copy
import z3

from slither.core.solidity_types.type import Type
from typing import Dict, List, Any
from slither.solc_parsing.variables.state_variable import StateVariableSolc
from geth_wrapper import DeploymentLogger
from web3 import Web3
from datetime import datetime
import logging

mmlog = logging.getLogger('magic_mirror')

def get_index_write_values(function, tc):
    # data_type => level => StateVariableSolc => value
    res: Dict[Type, Dict[int, Dict[StateVariableSolc, List[Any]]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for p_name, value in tc.items():
        param = function.get_parameter_by_name(p_name)
        if not param: continue
        for (level, SVs) in param.state_var_index_write.items():
            for sv in SVs:
                if value not in res[param.type][level][sv]:
                    res[param.type][level][sv].append(value)
    return res


def make_copy(index_values):
    res = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for data_type, levels in index_values.items():
        for level, SVs in levels.items():
            for sv, values in SVs.items():
                for value in values:
                    if value not in res[data_type][level][sv]:
                        res[data_type][level][sv].append(value)
    return res


class Transaction:
    def __init__(self, function, tc, parent_transaction, new_coverage, contract, logger):
        if logger.status != 1:
            raise Exception('Failed transaction should not have been created. ')

        self._function = function
        self._tc = tc
        self._parent = parent_transaction
        self._children = []
        self._index_values = get_index_write_values(function, tc)   # data_type => level => StateVariableSolc => value
        self._all_index_values = self._get_previous_index_values()
        self._new_coverage = new_coverage
        new_coverage_weight = 2 if new_coverage else 0
        self._weight = new_coverage_weight + 1
        self._depth = 0 if not parent_transaction else parent_transaction.depth + 1
        self._state_id = logger.tx_id
        self._is_deployment = True if isinstance(logger, DeploymentLogger) else False
        self._contract_address = Web3.toChecksumAddress(logger.deployed_address) if self._is_deployment else parent_transaction.contract_address
        self._can_enter_functions = None
        self.set_can_enter_functions(contract)
        self.vulnerabilities = []
        if parent_transaction:
            parent_transaction.add_child(self)

    def __str__(self):
        return f'{self.function if self.function else "constructor()"}  {self.tc}'

    def __repr__(self):
        return f'{self.function if self.function else "constructor()"}  {self.tc}'

    @property
    def state_id(self):
        return self._state_id

    @property
    def is_deployment(self):
        return self._is_deployment

    @property
    def contract_address(self):
        return self._contract_address

    @property
    def depth(self):
        return self._depth

    @property
    def can_enter_functions(self):
        return self._can_enter_functions

    def set_can_enter_functions(self, contract):
        res = []
        if self.function and self.function.is_suicidal:
            self._can_enter_functions = res
            return

        candidate_functions = contract.fuzzing_candidate_functions
        for function in candidate_functions:
            s = function.z3.solver
            s.push()
            function.z3.load_z3_state_values(self.state_id)
            if s.check() == z3.sat:
                res.append(function)
            s.pop()
        self._can_enter_functions = res

    def add_child(self, transaction):
        self._children.append(transaction)

    def _get_previous_index_values(self):
        res = make_copy(self.this_index_values_dic)
        temp = self.parent
        while temp:
            for data_type, levels in temp.previous_index_values_dic.items():
                for level, SVs in levels.items():
                    for sv, values in SVs.items():
                        for value in values:
                            if value not in res[data_type][level][sv]:
                                res[data_type][level][sv].append(value)
            temp = temp.parent
        return res

    @property
    def new_coverage(self):
        return self._new_coverage

    @property
    def weight(self):
        return self._weight

    @property
    def this_index_values_dic(self):
        return self._index_values

    @property
    def previous_index_values_dic(self):
        return self._all_index_values

    @property
    def parent(self):
        return self._parent

    @property
    def children(self):
        return self.children

    @property
    def function(self):
        return self._function

    @property
    def tc(self):
        return self._tc
