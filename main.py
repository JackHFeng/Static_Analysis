from slither import Slither
import globals
from core.classes.contract import Contract


def create_contract():
    for contract in globals.slither.contracts:
        n_contract = Contract(contract)
        globals.contracts.append(n_contract)


def main():
    contract_dir = './Purchase.sol'
    globals.slither = Slither(contract_dir)
    create_contract()

    # for contract in globals.contracts:
    #     for function in contract.functions.values():
    #         print(f'{function.name}')
    #         for sv in function.state_variables_read:
    #             print(f'\t{sv.name}')


if __name__ == '__main__':
    main()
