from slither import Slither

contract_dir = '/Users/jackfeng/Dropbox/Dropbox/CTFuzz/CTFuzz/ContractStudyCases/DocumentationExamples/Ballot.sol'
slither = Slither(contract_dir)

for contract in slither.contracts:
    for function in contract.functions:
        IRs = function.all_slithir_operations()
        print(function.name)

        for ir in IRs:
            print(f'\t{ir}')
            print(f'\t\t{type(ir)}')
