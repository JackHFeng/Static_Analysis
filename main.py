from static_analysis.data_dependency_graph import DDGs
from static_analysis.dependency_graph.dependency_graph import DependencyGraph


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
    data_dependency_graphs = DDGs(contract_dir)

    # getting the contract object by name.
    contract = data_dependency_graphs.get_contract_by_name(contract_name)
    print(contract.contract_summary())

    # Graph generation
    DG = DependencyGraph(contract)

    f = open(f'./_graphs/{contract_name}.html', 'w')
    f.write(DG.html)
    f.close()


if __name__ == '__main__':
    try:
        # # main('Ballot')
        #
        # l = ["Example", "Ballot", "Purchase", "ReceiverPays", "SimpleAuction", "BlindAuction", "Token"]
        # #l = ["Ballot"]
        #
        # for c in l:
        #     print(c)
        #     main(c)
        #
        import subprocess
        l = ["Ballot", "Purchase", "ReceiverPays", "SimpleAuction", "BlindAuction", "Token"]
        # subprocess.call(['solc', 'use', '0.5.11'])
        for c in l:
            main(c)

        # subprocess.call(['solc', 'use', '0.5.7'])
        # main('CryptoHands')
        #
        # subprocess.call(['solc', 'use', '0.4.25'])
        # main('CryptoMinerToken')
        #
        # subprocess.call(['solc', 'use', '0.4.24'])
        # main('lothlor')
        #
        # subprocess.call(['solc', 'use', '0.4.18'])
        # main('HoloToken')
        # main('WETH9')
        #
        # subprocess.call(['solc', 'use', '0.4.16'])
        # main('Exchange')
    except KeyboardInterrupt:
        pass