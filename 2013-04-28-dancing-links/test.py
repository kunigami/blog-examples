import unittest
from dancing import DancingLinks

class TestAlgorithmX(unittest.TestCase):

    def check(self, mat, expected):
        solver = DancingLinks(mat)
        solution = solver.solve()
        sets = [n.row for n in solution]
        sets.sort()
        self.assertEquals(expected, sets)
    
    def testSimpleIdentity(self):
        self.check([[1, 0], [0, 1]], [0, 1])

    def testPaperMatrix(self):
        mat = [[0, 0, 1, 0, 1, 1, 0],
               [1, 0, 0, 1, 0, 0, 1],
               [0, 1, 1, 0, 0, 1, 0],
               [1, 0, 0, 1, 0, 0, 0],
               [0, 1, 0, 0, 0, 0, 1],
               [0, 0, 0, 1, 1, 0, 1]]
        self.check(mat, [0, 3, 4])

if __name__ == '__main__':
    unittest.main()
