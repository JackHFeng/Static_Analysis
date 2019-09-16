from slither.slither import Slither
import collections

slither = Slither('/Users/jackfeng/Dropbox/Dropbox/CTFuzz/CTFuzz/ContractStudyCases/DocumentationExamples/Ballot.sol')

dic = collections.defaultdict(lambda: [[], []])

for contract in slither.contracts:
    print('Contract: ' + contract.name)

    for function in contract.functions:
        #print('Function: {}'.format(function.name))

        #print('\tRead: {}'.format([v.name for v in function.state_variables_read]))

        for v in function.state_variables_read:
            dic[v][1].append(function.name)

        #print('\tWritten {}'.format([v.name for v in function.state_variables_written]))

        for v in function.state_variables_written:
            dic[v][0].append(function.name)


    for k, v in dic.items():
        print(f'State Variable: {k}')
        print(f'\tWrote: {v[0]}')
        print(f'\tRead: {v[1]}')