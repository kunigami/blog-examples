from random import randint, seed

class SkipNode:
    """A node from a skip list"""    
    def __init__(self, height = 0, elem = None):
        self.elem = elem
        self.next = [None]*height

class SkipList:

    def __init__(self):
        self.head = SkipNode()
        self.len = 0
        self.maxHeight = 0

    def __len__(self):
        return self.len

    def find(self, elem):
        dummy, x = self.updateList(elem)
        return x

    def contains(self, elem):
        x = self.find(elem)        
        return x != None and x.elem == elem

    def randomHeight(self):
        height = 1
        while randint(1, 2) != 1:
            height += 1
        return height

    def updateList(self, elem):
        update = [None]*self.maxHeight
        x = self.head
        for i in reversed(range(self.maxHeight)):
            while x.next[i] != None and x.next[i].elem < elem:
                x = x.next[i]
            update[i] = x
        candidate = update[0].next[0] if len(update) > 0 else None
        return update, candidate
        
    def insert(self, elem):

        node = SkipNode(self.randomHeight(), elem)
        # Make sure that the head has at least the maximum level
        self.maxHeight = max(self.maxHeight, len(node.next))
        while len(self.head.next) < len(node.next):
            self.head.next.append(None)

        update, x = self.updateList(elem)            
        
        if x != None and x.elem == elem:
            return
        else:
            for i in range(len(node.next)):
                node.next[i] = update[i].next[i]
                update[i].next[i] = node
            self.len += 1

    def remove(self, elem):

        update, x = self.updateList(elem)

        if x != None and x.elem == elem:
            for i in reversed(range(len(x.next))):
                update[i].next[i] = x.next[i]
                if self.head.next[i] == None:
                    self.maxHeight -= 1
            self.len -= 1            
                
    def printList(self):
        for i in range(len(self.head.next)-1, -1, -1):
            x = self.head
            while x.next[i] != None:
                print x.next[i].elem,
                x = x.next[i]
            print ''
