from game import tictactoe as tic
from model import ticmodel, combine

first = ticmodel()
second = ticmodel()

for i in range(1000000):
    xox = tic(4)
    first, second = xox.train(first, second)

combined = combine(first, second, 'save-1m-3.json')
last = ticmodel(fname='save-1m-3.json')

xox = tic(4)
xox.vs(last)