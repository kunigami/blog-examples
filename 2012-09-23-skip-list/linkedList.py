class Node:

    def __init__(self, elem):
        self.elem = elem
        self.next = None

class LinkedList:

    def __init__(self):

        self.head = Node(None)
        self.len = 0

    def __len__(self):
        return self.len

    def find(self, elem):
        x = self.head
        while x.next != None and x.next.elem <= elem:
            x = x.next
        return x

    def insert(self, elem):
        x = self.find(elem)
        if x.elem == elem:
            return

        node = Node(elem)
        node.next = x.next
        x.next = node

        self.len += 1

    def printList(self):
        x = self.head.next
        while x != None:
            print x.elem,
            x = x.next
        print ''
