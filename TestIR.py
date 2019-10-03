from slither import Slither
from slither.slithir.operations.binary import Binary
contract_dir = './Ballot.sol'
slither = Slither(contract_dir)

for contract in slither.contracts:
    for function in contract.functions:
        IRs = function.all_slithir_operations()
        print(function.name)

        for ir in IRs:
            print(f'\t{ir}')
            print(f'\t\t{type(ir)}')
            if isinstance(ir, Binary):
                print(f'\t\t{ir.type_str}')
