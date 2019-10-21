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
 
if __name__ == '__main__':

    unittest.main()
