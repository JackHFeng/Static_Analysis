from core.contracts import Contracts
from core.dependency_graph.dependency_graph import DependencyGraph
from core.select_solc_compiler import set_version


def main(contract_dir, contract_name):

    """
    ReceiverPays does not show owner. 
    WETH9 does not show requires. 
    Ballot does not show requires. 
    """

    # constructs the data dependency graph.
    # if a file contains multiple contracts, DDG will be constructed for each.
    contracts = Contracts(contract_dir)

    # getting the contract object by name.
    contract = contracts.get_contract_by_name(contract_name)
    print(contract.summary)

    # Graph generation
    DG = DependencyGraph(contract)

    f = open(f'./_graphs/{contract_name}.html', 'w')
    f.write(DG.html)
    f.close()


if __name__ == '__main__':
    try:
        contracts = ["Purchase", "Ballot", "ReceiverPays", "SimpleAuction", "BlindAuction", "Token", "Example",
                     "CryptoHands", "CryptoMinerToken", "lothlor", "HoloToken", "WETH9", "Exchange"]

        for contract in contracts:
            source_dir = f'./_sample_contracts/{contract}.sol'
            set_version(source_dir)
            main(source_dir, contract)


        # l = ["Ballot", "Purchase", "ReceiverPays", "SimpleAuction", "BlindAuction", "Token", "Example"]
        # select_solc('0.5.11')
        # for c in l:
        #     main(c)
        #
        # select_solc('0.5.7')
        # main('CryptoHands')
        #
        # select_solc('0.4.25')
        # main('CryptoMinerToken')
        #
        # select_solc('0.4.24')
        # main('lothlor')
        #
        # select_solc('0.4.18')
        # main('HoloToken')
        # main('WETH9')
        #
        # select_solc('0.4.16')
        # main('Exchange')
    except KeyboardInterrupt:
        pass