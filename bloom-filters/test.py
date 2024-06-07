import unittest
from bloom import BloomFilter

class TestBloomFilter(unittest.TestCase):

    def testFalseNegativeNeverHappens(self):
        n = 10
        inserted = []
        bf = BloomFilter(n, n)
        for i in range(n):
            bf.insert(str(i))
            inserted.append(i)
            for j in inserted:
                self.assertTrue(bf.query(j))

    def testNumberOfSetBitsNeverDecreases(self):
        n = 10
        bf = BloomFilter(n, n)
        prev_cnt = 0
        for i in range(n):
            bf.insert(str(i))
            cnt = bf.count(True)
            self.assertTrue(cnt >= prev_cnt)
            prev_cnt = cnt

    def testInputIsFalsePositiveUntilInserted(self):
        n = 100
        bf = BloomFilter(int(n/2), n)
        fp = [False]*n
        inserted = [False]*n
        fp_cnt = 0
        for i in range(n):
            bf.insert(str(i))
            inserted[i] = True
            for j in range(n):
                if inserted[j]:
                    continue
                # It was false positive before, it must continue
                # to be (since it was not inserted).
                if fp[j]:
                    self.assertTrue(bf.query(j))
                # Update false positives list
                elif bf.query(j):
                    fp[j] = True
                    fp_cnt += 1
        # We're inserting more elements than the size of the array, so
        # there must be false positives.
        self.assertTrue(fp_cnt > 0)


if __name__ == '__main__':
    unittest.main()
