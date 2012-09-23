from skipList import SkipList
from linkedList import LinkedList
import unittest
from random import seed, randint
from timeit import Timer

class SkipListTest(unittest.TestCase):

    def setUp(self):
        seed(0)
        self.sl = SkipList()

    # Test insert(elem)
 
    def testInsertionInEmptyList(self):
        self.sl.insert(1)
        self.assertTrue(self.sl.contains(1))
        self.assertFalse(self.sl.contains(2))

    def testInsersionAtTheBeginningOfTheList(self):
        self.sl.insert(2)
        self.sl.insert(1)
        self.assertTrue(self.sl.contains(1))
        self.assertTrue(self.sl.contains(2))
        
    def testInsersionAtTheEndOfTheList(self):
        self.sl.insert(1)
        self.sl.insert(2)
        self.assertTrue(self.sl.contains(1))
        self.assertTrue(self.sl.contains(2))

    def testInsertionOfTheSameElement(self):
        self.sl.insert(1)
        self.sl.insert(1)
        self.assertTrue(self.sl.contains(1))
        self.assertEqual(1, len(self.sl))

    # Test remove(elem)

    def testRemovalFromASingleElementList(self):
        self.sl.insert(1)
        self.assertTrue(self.sl.contains(1))
        self.sl.remove(1)
        self.assertFalse(self.sl.contains(1))

    def testRemovalFromAnElementNotInTheList(self):
        self.sl.remove(1)
        self.sl.insert(1)
        self.assertTrue(self.sl.contains(1))
        self.sl.remove(2)
        self.assertTrue(self.sl.contains(1))

    # Test find(elem)

    def testFindingOfASingleElementList(self):
        self.sl.insert(1)
        node = self.sl.find(1)
        self.assertEqual(1, node.elem)

    def testFindingOfTheMiddleElementList(self):
        self.sl.insert(1)
        self.sl.insert(2)
        self.sl.insert(3)
        node = self.sl.find(2)
        self.assertEqual(2, node.elem)

    def testFindingAnElementNotInTheList(self):
        self.assertEqual(None, self.sl.find(1))

    def testInsertion(self):
        # l = LinkedList()
        # for i in range(N):
        #     l.insert(randint(1, N))
        print 'Inserting 10000 elements in a Skip List'
        # Test execution time for a O(log n) operations
        print 'Execution time:  %.2fs' % (Timer(self.insertManyElementsInSkipList).timeit(number=2))
        print 'Number of elements: %d' % (len(self.sl))
        print 'Number of nodes:    %d' % (self.sl.nodes)

        print 'Inserting 10000 elements in a Linked List'
        print 'Execution time: %.2fs' % (Timer(self.insertManyElementsInLinkedList).timeit(number=1))
        
    def insertManyElementsInSkipList(self):
        N = 10000
        for i in range(N):
            self.sl.insert(randint(1, N))
            
    def insertManyElementsInLinkedList(self):
        N = 10000
        l = LinkedList()
        for i in range(N):
            l.insert(randint(1, N))
        print 'Number of elements: %d' % (len(l))

def insertElements():
    N = 10000
    sl = SkipList()
    for i in range(N):
        sl.insert(randint(1, N))
 
if __name__ == '__main__':

    unittest.main()
