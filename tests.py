__author__ = 'ola'
import main
from itertools import permutations

goodsolution = [1, 0]
assert main.isGoodSolution(goodsolution)

gs = goodsolution

i = 0
perm = permutations(goodsolution)
next(perm)
while i < 10:
    (gs, perm) = main.findNextSolution(gs, perm)
    print(gs)
    i += 1


