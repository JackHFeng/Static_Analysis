from slither import Slither
from .declarations.contract import Contract


class Contracts:
    def __init__(self, _dir: str):
        self.contracts = {}
        slither = Slither(_dir)
        for contract in slither.contracts:
            new_contract = Contract(contract)
            self.contracts[contract.name] = new_contract

    def get_contract_by_name(self, _name: str):
        return self.contracts.get(_name)

