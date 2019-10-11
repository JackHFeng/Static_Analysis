from core.data_dependency_graph import DDGs


def main():
    contract_dir = './Ballot.sol'
    data_dependency_graphs = DDGs(contract_dir)
    contract = data_dependency_graphs.get_contract_by_name('Purchase')
    print(contract)


if __name__ == '__main__':
    main()
