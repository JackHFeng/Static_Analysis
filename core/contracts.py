from slither import Slither
from .declarations.contract import Contract
import re
from definitions import ROOT_DIR


def get_sol_version(dir):
    version = None
    code = open(dir, 'r', encoding='utf-8').read().split('\n')
    for line, content in enumerate(code):
        if 'pragma solidity' in content:
            version = re.findall(r'[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}', content)[0]
    return version


def get_all_solc_versions():
    from os import listdir
    from os.path import join, isdir

    solc_dir = f'{ROOT_DIR}/solc/'
    solc_versions = [f for f in listdir(solc_dir) if isdir(join(solc_dir, f))]
    return solc_versions


def compiler_source(_dir):
    sol_version = get_sol_version(_dir)
    all_sol_versions = get_all_solc_versions()
    if sol_version:
        all_sol_versions.remove(sol_version)
        all_sol_versions.insert(0, sol_version)
    for version in all_sol_versions:
        try:
            slither = Slither(_dir, solc=f'{ROOT_DIR}/solc/{version}/solc.exe')
            return version, slither
        except:
            pass
    raise Exception(f'Existing solidity compilers do not work on "{_dir}"')


class Contracts:
    def __init__(self, _dir: str):
        self.contracts = {}
        slither = compiler_source(_dir)
        for contract in slither.contracts:
            new_contract = Contract(contract)
            self.contracts[contract.name] = new_contract

    def get_contract_by_name(self, _name: str):
        return self.contracts.get(_name)

