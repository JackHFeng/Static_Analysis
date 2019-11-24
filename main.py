from core.data_dependency_graph import DDGs


def main():

    # name of contract.
    contract_name = "ReceiverPays"

    """
    ReceiverPays does not show owner. 
    WETH9 does not show requires. 
    Ballot does not show requires. 
    """

    # the name of contract is used as file name to find the sol file in the root directory.
    contract_dir = f'./{contract_name}.sol'

    # constructs the data dependency graph.
    # if a file contains multiple contracts, DDG will be constructed for each.
    data_dependency_graphs = DDGs(contract_dir)

    # getting the contract object by name.
    contract = data_dependency_graphs.get_contract_by_name(contract_name)
    print(contract)


if __name__ == '__main__':
    main()
