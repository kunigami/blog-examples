import unittest
from queue_list import *

class TestQueueList(unittest.TestCase):
    def test_empty_queue(self):
        q = QueueList()
        self.assertTrue(q.isEmpty())

    def test_inserting_to_queue(self):
        q = QueueList()
        q.push(1)
        self.assertFalse(q.isEmpty())
        e = q.pop()
        self.assertEqual(e, 1)
        # Check that element got removed
        self.assertTrue(q.isEmpty())

    def test_removing_from_empty_queue(self):
        q = QueueList()
        with self.assertRaises(RuntimeError):
            q.pop()

    def test_inserting_multiple_to_queue(self):
        q = QueueList()
        q.push(1)
        q.push(2)
        q.push(3)

        l = []
        while not q.isEmpty():
            l.append(q.pop())
        self.assertEqual(l, [1, 2, 3])


if __name__ == '__main__':
    unittest.main()
