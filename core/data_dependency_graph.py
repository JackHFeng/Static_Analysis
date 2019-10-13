from slither import Slither
from .declarations.contract import Contract


class DDGs:
    def __init__(self, dir: str):
        self.contracts = {}
        slither = Slither(dir)
        for contract in slither.contracts:
            new_contract = Contract(contract)
            self.contracts[contract.name] = new_contract

    def get_contract_by_name(self, name: str):
        return self.contracts.get(name)
