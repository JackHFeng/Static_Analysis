from core.contracts import Contracts
from core.dependency_graph.dependency_graph import DependencyGraph


def main(_contract_name):

    # name of contract.
    # contract_name = "ReceiverPays"
    contract_name = _contract_name

    """
    ReceiverPays does not show owner. 
    WETH9 does not show requires. 
    Ballot does not show requires. 
    """
    # the name of contract is used as file name to find the sol file in the root directory.
    contract_dir = f'./_sample_contracts/{contract_name}.sol'

    # constructs the data dependency graph.
    # if a file contains multiple contracts, DDG will be constructed for each.
    contracts = Contracts(contract_dir)

    # getting the contract object by name.
    contract = contracts.get_contract_by_name(contract_name)
    print(contract.contract_summary())

    # Graph generation
    DG = DependencyGraph(contract)

    f = open(f'./_graphs/{contract_name}.html', 'w')
    f.write(DG.html)
    f.close()


def select_solc(version):
    import os
    if os.name == 'nt':
        from core.windows_sol_select import set_solc_version
        set_solc_version(src_dir='E:/Desktop/solc', dst_dir='E:/Desktop/solc/current', version=version)

    elif os.name == "posix":
        import subprocess
        subprocess.call(['solc', 'use', version])


if __name__ == '__main__':
    try:

        l = ["Ballot", "Purchase", "ReceiverPays", "SimpleAuction", "BlindAuction", "Token", "Example"]
        select_solc('0.5.11')
        for c in l:
            main(c)

        select_solc('0.5.7')
        main('CryptoHands')

        select_solc('0.4.25')
        main('CryptoMinerToken')

        select_solc('0.4.24')
        main('lothlor')

        select_solc('0.4.18')
        main('HoloToken')
        main('WETH9')

        select_solc('0.4.16')
        main('Exchange')
    except KeyboardInterrupt:
        pass