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
    contract_dir = './Purchase.sol'
    globals.slither = Slither(contract_dir)
    createContract()


if __name__ == '__main__':
    main()