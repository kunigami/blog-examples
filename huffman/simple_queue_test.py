import unittest
from simple_queue import Queue

class QueueTest(unittest.TestCase):

    def test_operations(self):
        q = Queue()
        self.assertTrue(q.is_empty())
        self.assertEqual(q.front(), None)
        self.assertEqual(q.pop(), None)

        q.push(1)
        self.assertFalse(q.is_empty())
        self.assertEqual(q.front(), 1)

        q.push(2)
        self.assertEqual(q.front(), 1)

        val = q.pop()
        self.assertEqual(val, 1)
        self.assertEqual(q.front(), 2)

        val = q.pop()
        self.assertEqual(val, 2)
        self.assertTrue(q.is_empty())


    def test_initialized_queue(self):
        init = [1, 2, 3, 4, 5]
        q = Queue([1, 2, 3, 4, 5])
        arr = get_array(q)
        self.assertEqual(arr, init)

    def test_multiple_queues(self):
        q1 = Queue()
        q2 = Queue()

        q1.push(1)
        q2.push(2)

        self.assertEqual(get_array(q1), [1])
        self.assertEqual(get_array(q2), [2])

def get_array(q):
    arr = []
    while not q.is_empty():
        arr.append(q.pop())
    return arr

if __name__ == '__main__':

    unittest.main()
