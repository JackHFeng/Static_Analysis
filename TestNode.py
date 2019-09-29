from slither import Slither

contract_dir = '/Users/jackfeng/Dropbox/Dropbox/CTFuzz/CTFuzz/ContractStudyCases/DocumentationExamples/Ballot.sol'
slither = Slither(contract_dir)

for contract in slither.contracts:
    print(contract.name)
    for function in contract.functions:
        print(function.name)

        for node in function.nodes:

            print(f'\t{node.expression}\n')
            print(f'\t\t variables read:')
            for variable in node.variables_read:
                print(f'\t\t\t{variable.name}')

            print(f'\t\t variables write:')
            for variable in node.variables_written:
                print(f'\t\t\t{variable.name}')

            print(f'\t\t state variables read:')
            for variable in node.state_variables_read:
                print(f'\t\t\t{variable.name}')

            print(f'\t\t state variables write:')
            for variable in node.state_variables_written:
                print(f'\t\t\t{variable.name}')
