from core.data_dependency_graph import DDGs


def main():
    contract_dir = './Ballot.sol'
    data_dependency_graphs = DDGs(contract_dir)
    contract = data_dependency_graphs.get_contract_by_name('Ballot')

    # for sv in contract.state_variables.values():
    #     print(f'{sv.name} {sv.set_by_constructor}')
    # for fn in contract.functions.values():
    #     print(fn.name)
    #     svs = fn.state_variables_read
    #     for sv in svs:
    #         print('\t' + sv.name)
    #         fs = fn.get_depended_functions_by_state_variable(sv.name)
    #         for f in fs:
    #             print(f'\t\t{f.name}')


if __name__ == '__main__':
    main()
