## https://stackoverflow.com/questions/13395391/z3-finding-all-satisfying-models
## Z3 is stateful, same solver object is faster

## https://stackoverflow.com/questions/11867611/z3py-checking-all-solutions-for-equation
## Answer provided by autheor of z3



# https://ericpony.github.io/z3py-tutorial/guide-examples.htm
# http://www.cs.tau.ac.il/~msagiv/courses/asv/z3py/
from z3 import *
import random
import time
print(f'****Solving example')
set_param("auto-config",False)
set_param("smt.phase-selection",5)
set_param("smt.arith.random_initial_value",True)
set_param("smt.random_seed", 2)
set_param("sat.phase", 'random')
set_param("sat.random_seed", 2)
x = Int('x')
y = Int('y')
s = Solver()
s.add(x + y > 0)
s.check()
m = s.model()
print(m[x])
print(m[y])

 
#


# s = Solver()
# x = Int('x')
# y = Int('y')
# F = [x > 2, y < 10]
# s.add(F)
#
# if s.check() == sat:
#     m = s.model()
#     m.decls()
#     print(m[x])
#     print(m[y])


print(f'\n****Simplifier example')
x = Int('x')
y = Int('y')
print(simplify(x + y + 2*x + 3))
print(simplify(x < y + x + 2))
print(simplify(And(x + 1 >= 3, x**2 + x**2 + y**2 + 2 >= 5)))

print(f'\n****Traversing Expression example')
x = Int('x')
y = Int('y')
n = x + y >= 3
##  similar to AST expression available within slither.
print("num args: ", n.num_args())
print("children: ", n.children())
print("1st child:", n.arg(0))
print("2nd child:", n.arg(1))
print("operator: ", n.decl())
print("op name:  ", n.decl().name())


x = Int('x')
y = Int('y')
f = Function('f', IntSort(), IntSort())
solve(f(f(x)) == x, f(x) == y, x != y)


command = "(set-option :smt.arith.random_initial_value true)\n" \
          "(declare-const x Int)\n" \
          "(declare-const y Int)\n" \
          "(assert (> (+ x y) 0))\n"


# x = Int('x')
# y = Int('y')
# s = "x > y"
# f2 = eval(s)
# solve(f2)

named_v = {'a1' : Int('a1'), 'a2': Int('a2'), 'a3' : Int('a3')}
# solve(namedclass['a1'] > namedclass['a2'], namedclass['a2'] != namedclass['a3'])
s = "And(named_v['a1'] > named_v['a2'])"
f2 = eval(s)
solver = Solver()
solver.add(f2)
print(solver.check())
m = solver.model()
print(f'a1:{m[named_v["a1"]]}')
print(f'a2:{m[named_v["a2"]]}')


print('\nExample: Require(a > b)')

