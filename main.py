from slither import Slither
import globals
from core.classes.contract import Contract


def createContract():
    for contract in globals.slither.contracts:
        n_contract = Contract()
        globals.contracts.append(n_contract)

        n_contract.name = contract.name

        for function in contract.functions:
            n_contract.create_function(function)

        for modifier in contract.modifiers:
            n_contract.create_modifier(modifier)


def main():
    contract_dir = './HoloToken.sol'
    globals.slither = Slither(contract_dir)
    createContract()
    globals.contracts[0].functions[0]

    for contract in globals.contracts:
        for function in contract.functions:
            print(f'{function.name}')
            for sv in function.state_variables_read:
                print(f'\t{sv.name}')


if __name__ == '__main__':
    main()