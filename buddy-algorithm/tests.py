import random
import unittest

from buddy_algorithm import \
    Allocator, \
    MAX_SIZE_CLASS, \
    MIN_SIZE_CLASS, \
    buddy_address

class BuddyAlgorithmTest(unittest.TestCase):

    def testInitialMemory(self):
        allocator = Allocator()
        histo = allocator.get_histogram()
        self.assertEqual(histo[MAX_SIZE_CLASS], 1)

    def testAllocatingTinyMemory(self):
        allocator = Allocator()
        allocator.alloc(1)
        histo = allocator.get_histogram()
        expected_histo = {}
        for k in range(MIN_SIZE_CLASS, MAX_SIZE_CLASS):
            expected_histo[k] = 1
        self.assertEqual(histo, expected_histo)

    def testAllocAndFree(self):
        allocator = Allocator()
        addr = allocator.alloc(1)
        allocator.free(addr)

        histo = allocator.get_histogram()
        self.assertEqual(histo[MAX_SIZE_CLASS], 1)

    def testAllocAndFree2(self):
        allocator = Allocator()
        addr1 = allocator.alloc(1)
        addr2 = allocator.alloc(1000)

        allocator.free(addr2)
        allocator.free(addr1)

        histo = allocator.get_histogram()
        self.assertEqual(histo[MAX_SIZE_CLASS], 1)

    def testAllocatingMaxMemory(self):
        max_mem = 2**MAX_SIZE_CLASS
        allocator = Allocator()
        # It should file to allocate exactly the max memory
        # since some of it is used for metadata
        with self.assertRaises(Exception):
            allocator.alloc(max_mem)

    def testAllocatingAlmostMaxMemory(self):
        max_mem = 2**MAX_SIZE_CLASS - 100
        allocator = Allocator()
        allocator.alloc(max_mem)
        histo = allocator.get_histogram()
        # No blocks are available
        self.assertEqual(histo, {})

    def testAllocations1(self):
        sizes = [851, 440, 987, 119, 522]
        allocator = Allocator()
        addresses = []
        for size in sizes:
            addresses.append(allocator.alloc(size))


        for addr in addresses:
            allocator.free(addr)

    def testRandomAllocations(self):
        allocator = Allocator()
        addresses = []
        for i in range(5):
            random_size = random.randint(100, 2**(MAX_SIZE_CLASS/2))
            addr = allocator.alloc(random_size)
            addresses.append(addr)

        # Deallocate all memory
        for addr in addresses:
            allocator.free(addr)

        histo = allocator.get_histogram()
        print(histo)
        self.assertEqual(histo[MAX_SIZE_CLASS], 1)


class MemoryTest(unittest.TestCase):

    def testRightBuddyAddress(self):
        class_size = MIN_SIZE_CLASS + 2
        addr = 0
        buddy_addr = buddy_address(addr, class_size)
        self.assertEqual(buddy_addr, 2**class_size)

    def testLeftBuddyAddress(self):
        class_size = MIN_SIZE_CLASS + 2
        addr = 2**class_size
        buddy_addr = buddy_address(addr, class_size)
        self.assertEqual(buddy_addr, 0)

    def testRightBuddyAddress2(self):
        class_size = MIN_SIZE_CLASS + 2
        addr = 2**class_size
        buddy_addr = buddy_address(addr, class_size - 1)
        self.assertEqual(buddy_addr, 3*(2**(class_size - 1)))

if __name__ == '__main__':
    unittest.main()
