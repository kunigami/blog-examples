import unittest
from aho_corasick import search


class TestAhoCorasick(unittest.TestCase):

    def testNoMatches(self):
        matches = search('aaaaaaaad', ['b', 'c', 'dd'])
        self.assertEquals([], matches)

    def testSingleMatch(self):
        matches = search('aabaaa', ['b', 'bb', 'bbb'])
        self.assertEquals([(2, 3)], matches)

    def testManyMatches(self):
        matches = search('aaaa', ['a', 'aa', 'aaa'])
        self.assertEquals([(0, 1), (0, 2), (1, 2), (0, 3),
                           (1, 3), (2, 3), (1, 4), (2, 4), (3, 4)], matches)


if __name__ == '__main__':
    unittest.main()
