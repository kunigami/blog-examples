from bitarray import bitarray
from pyhash import murmur3_x64_128
from math import log

class BloomFilter:
    def __init__(self, size, num_values):
        """Simple implementation of a Bloom filter.

        It stores a bit array internally of @size bits and expects
        @num_values to be inserted.

        @size - how many bits the bitarray has. the larger the less the
        chance of a false positive

        @num_values - number of distinct values we expect to insert/query
        in the bloom filter

        """
        self.size = size
        self.bitArr = bitarray(size)
        self.bitArr.setall(False)
        self.hasher = murmur3_x64_128()

        # Number of hash functions that minimizes the
        # probability of false positives
        self.numHashes = max(5, int(log(2)*size/num_values))
        self.numHashes = 2

    def insert(self, value):
        hashes = self.__getHashes(value)
        for h in hashes:
            self.bitArr[h] = True

    def query(self, value):
        hashes = self.__getHashes(value)
        #print value, hashes
        return all(map(lambda h: self.bitArr[h], hashes))

    def count(self, boolean):
        return self.bitArr.count(boolean)

    def __getHashes(self, value):
        h128 = self.hasher(str(value))
        h64l = h128 & ((1L << 64) - 1)
        h64u = h128 >> 64

        hashes = map(
            lambda i: (h64l + i*h64u) % self.size,
            range(self.numHashes)
        )
        return hashes

    def __str__(self):
        return self.bitArr.to01()
