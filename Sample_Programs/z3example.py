from z3 import *

I = IntSort()
# A is an array from integer to integer
A = Array('A', I, I)
x = Int('x')
print(f'A[x]: {A[x]}')
s = Solver()
s.add(A[0] == 0, A[1] == 1, A[x] == 1, x == 0)
print(f's.check(): {s.check()}')
print(f's.model()[x].as_long(): {s.model()[x].as_long()}')
