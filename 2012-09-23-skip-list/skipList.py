from random import randint, seed

class SkipNode:
    """A node from a skip list"""
    
    def __init__(self, elem):
        self.elem = elem
        # Decide how many levels this node will have
        self.height = 1
        while randint(1, 2) != 1:
            self.height += 1  
        self.prev = [None]*self.height
        self.next = [None]*self.height

class SkipList:

    
    def __init__(self):
        self.heads = []
        self.len = 0
        self.nodes = 0

    def __len__(self):
        return self.len

    def link(self, left, right, depth):
        left.next[depth] = right
        right.prev[depth] = left

    def contains(self, elem):
        x = self.find(elem)
        return x != None and x.elem == elem

    # Returns the a SkipNode with the greatest value that is smaller or equal to 'elem' 
    def find(self, elem):

        lvl = len(self.heads) - 1
        x = self.heads[-1] if len(self.heads) > 0 else None

        while lvl >= 0:

            y = None
            while x != None and x.elem <= elem:
                y = x
                x = x.next[lvl]

            # Element was found
            if y != None and y.elem == elem:
                return y
            # Bottom reached without finding the element
            # return the node with greatest value smaller than 'elem'
            if lvl == 0:
                return y

            lvl -= 1
            if y != None:
                x = y
            else:
                x = self.heads[lvl]
        
    def insert(self, elem):

        x = self.find(elem)
        # Element is already present in the list, nothing to do...
        if x != None and x.elem == elem:
            return

        node = SkipNode(elem)
        # Make sure all levels up the maximum have a head
        while len(self.heads) < node.height:
            self.heads.append(None)

        for i in range(node.height):

            if x == None:
                # Inserting in the beginning of the list
                if self.heads[i] != None:
                    h = self.heads[i]
                    self.link(node, h, i)
                self.heads[i] = node
            else:
                y = x.next[i]
                if y != None:
                    self.link(node, y, i)
                self.link(x, node, i)

            # Find the candidate for the next level
            while x != None and x.height == i + 1:
                x = x.prev[i]

        self.len += 1
        self.nodes += node.height

    # Removes an element from the list
    def remove(self, elem):
        x = self.find(elem)
        
        # elem is not present in the current list. Nothing to do...
        if x == None or x.elem != elem:
            return False

        for i in range(x.height - 1, -1, -1):
            p = x.prev[i]
            n = x.next[i]
            if p != None:
                p.next[i] = n
            else:
                self.heads[i] = n

            if n != None:
                n.prev[i] = p

            # List is empty now
            if self.heads[i] == None:
                self.heads.pop()

        self.len -= 1
        self.nodes -= x.height
        return True

                
    def printList(self):
        print 'skip list'
        for i in range(len(self.heads)-1, -1, -1):
            x = self.heads[i]
            while x != None:
                print x.elem,
                if x == x.next[i]:
                    print 'error!!!'
                    exit(0)
                x = x.next[i]
            print ''



