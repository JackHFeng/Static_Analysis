from slither.slither import Slither
import collections


import os
import logging
import argparse
from slither import Slither
from slither.printers.all_printers import PrinterCallGraph
from slither.core.declarations.function import Function

logging.basicConfig()
logging.getLogger("Slither").setLevel(logging.INFO)
logging.getLogger("Printers").setLevel(logging.INFO)

class PrinterCallGraphStateChange(PrinterCallGraph):

    def _process_function(self, contract, function, contract_functions, contract_calls, solidity_functions, solidity_calls, external_calls, all_contracts):
        if function.view or function.pure:
            return
        super()._process_function(contract, function, contract_functions, contract_calls, solidity_functions, solidity_calls, external_calls, all_contracts)

    def _process_internal_call(self, contract, function, internal_call, contract_calls, solidity_functions, solidity_calls):
        if isinstance(internal_call, Function):
            if internal_call.view or internal_call.pure:
                return
        super()._process_internal_call(contract, function, internal_call, contract_calls, solidity_functions, solidity_calls)

    def _process_external_call(self, contract, function, external_call, contract_functions, external_calls, all_contracts):
        if isinstance(external_call[1], Function):
            if external_call[1].view or external_call[1].pure:
                return
        super()._process_external_call(contract, function, external_call, contract_functions, external_calls, all_contracts)

def parse_args():
    """
    """
    parser = argparse.ArgumentParser(description='Call graph printer. Similar to --print call-graph, but without printing the view/pure functions',
                                     usage='call_graph.py filename')

    parser.add_argument('filename',
                        help='The filename of the contract or truffle directory to analyze.')

    parser.add_argument('--solc', help='solc path', default='solc')

    return parser.parse_args()

slither = Slither('/Users/jackfeng/Dropbox/Dropbox/CTFuzz/CTFuzz/ContractStudyCases/DocumentationExamples/Ballot.sol')

dic = collections.defaultdict(lambda: [[], []])

for contract in slither.contracts:
    print('Contract: ' + contract.name)

    for function in contract.functions:
        print('Function: {}'.format(function.name))

        print('\tRead: {}'.format([v.name for v in function.state_variables_read]))

        for v in function.state_variables_read:
            dic[v][1].append(function.name)

        #print('\tWritten {}'.format([v.name for v in function.state_variables_written]))

        for v in function.state_variables_written:
            dic[v][0].append(function.name)


    for k, v in dic.items():
        print(f'State Variable: {k}')
        print(f'\tWrote: {v[0]}')
        print(f'\tRead: {v[1]}')

        var = contract.get_state_variable_from_name(k)
        functions_reading_var = contract.get_functions_reading_from_variable(var)
        function_using_var_as_condition = [f for f in functions_reading_var if \
                                         f.is_reading_in_conditional_node(var) or \
                                         f.is_reading_in_require_or_assert(var)]
        print(f'The function using "{k}" in condition are {[f.name for f in function_using_var_as_condition]}')

    # slither = Slither('/Users/jackfeng/Dropbox/Dropbox/CTFuzz/CTFuzz/ContractStudyCases/DocumentationExamples/Ballot.sol')
    #
    # slither.register_printer(PrinterCallGraphStateChange)
    #
    # slither.run_printers()



