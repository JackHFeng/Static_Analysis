from core.data_dependency_graph import DDGs
from slither.core.expressions.binary_operation import BinaryOperation
from slither.core.expressions.identifier import Identifier
from slither.core.expressions.literal import Literal
from z3 import *


def main():
    contract_dir = './Example.sol'
    data_dependency_graphs = DDGs(contract_dir)
    contract = data_dependency_graphs.get_contract_by_name('Example')

    for f in contract.functions.values():
        named_v = {}
        for r in f.requires:
            get_expr(r.operation, named_v)
            print(str(r.operation))
            s = Solver()
            constraints = r.code.split('(')[-1][:-1].split(' ')
            for i, v in enumerate(constraints):
                if v.isalpha():
                    constraints[i] = "named_v['" + v + "']"
            constraints = ' '.join(constraints)
            print(constraints)
            f = eval(constraints)
            f1 = eval("And(named_v['a'] != 0, named_v['b'] != 1)")
            s.add(f)
            s.add(f1)
            s.check()
            m = s.model()
            for k, v in named_v.items():
                print(f'{k}: {m[v]}')


def get_expr(op, dic):

    if isinstance(op, BinaryOperation):
        get_expr(op.expression_left, dic)
        get_expr(op.expression_right, dic)
    elif isinstance(op, Identifier):
        dic[op.value.name] = Int(op.value.name)

if __name__ == '__main__':
    main()