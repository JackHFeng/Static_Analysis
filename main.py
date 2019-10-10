from slither import Slither
import globals
from core.DataDependencyGraph.contract import Contract


def create_contract():
    for contract in globals.slither.contracts:
        n_contract = Contract(contract)
        globals.contracts.append(n_contract)


def main():
    contract_dir = './Ballot.sol'
    globals.slither = Slither(contract_dir)
    create_contract()

    for contract in globals.contracts:
        print(contract)


if __name__ == '__main__':
    main()
