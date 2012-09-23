class Node:

    def __init__(self, elem):
        self.elem = elem
        self.next = None

class LinkedList:

    def __init__(self):

        self.head = None
        self.len = 0

    def __len__(self):
        return self.len

    def find(self, elem):
        x = self.head
        y = None
        while x != None and x.elem <= elem:
            y = x
            x = x.next
        return y

    def insert(self, elem):
        node = Node(elem)

        y = self.find(elem)
        
        if y != None and y.elem == elem:
            return
        
        if y == None:
            node.next = self.head
            self.head = node
        else:
            node.next = y.next
            y.next = node

        self.len += 1

    def printList(self):
        x = self.head
        while x != None:
            print x.elem,
            x = x.next
        print ''

if __name__ == '__main__':
    l = LinkedList()
    l.insert(1)
    l.insert(3)
    l.insert(2)
    l.insert(-1)
    l.printList()
