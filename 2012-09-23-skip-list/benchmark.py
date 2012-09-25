from random import randint, seed
from skipList import SkipList
from rbTree import rbtree
from linkedList import LinkedList

from time import clock

def randomSequence(n):
    seed(0)
    i = 0
    while i < n:
        yield randint(1, n)
        i += 1
        
def increasingSequence(n):
    i = 0
    while i < n:
        yield i
        i += 1

def decreasingSequence(n):
    i = n-1
    while i >= 0:
        yield i
        i -= 1
    
def insertions(structure, generator):
    for s in generator:
        structure.insert(s)

def benchmarkOperation(structure, op, seq):
    start = clock()
    op(structure, seq)
    return (clock() - start)

def benchmark(generator):

    seq = list(generator)

    sl = SkipList()
    slt = benchmarkOperation(sl, insertions, seq)
    
    rbt = rbtree()
    rbtt = benchmarkOperation(rbt, insertions, seq)

    l = LinkedList()
    lt = benchmarkOperation(l, insertions, seq)

    print '%.2lf & %.2lf & %.2lf\\\\' % (slt, rbtt, lt)

benchmark(randomSequence(10000))
benchmark(increasingSequence(10000))
benchmark(decreasingSequence(10000))
