class Node:
    def __init__(self, row, col):
        self.row, self.col = row, col

    def deattach(self):
        self.up.down = self.down
        self.down.up = self.up
        
    def attach(self):
        self.down.up = self.up.down = self
        
class Head:
    def __init__(self, col):
        self.col = col

    def deattach(self):
        self.left.right = self.right
        self.right.left = self.left
        
    def attach(self):
        self.right.left = self.left.right = self

class NodeIterator:

    def __init__(self, node):
        self.curr = self.start = node

    def __iter__(self):
        return self

    def next(self):
        _next = self.move(self.curr)
        if _next == self.start:
            raise StopIteration
        else:
            self.curr = _next
            return _next

    def move(self):
        raise NotImplementedError

class LeftIterator (NodeIterator):
    def move(self, node):
        return node.left

class RightIterator (NodeIterator):
    def move(self, node):
        return node.right

class DownIterator (NodeIterator):
    def move(self, node):
        return node.down

class UpIterator (NodeIterator):
    def move(self, node):
        return node.up
    
class SparseMatrix:

    def createLeftRightLinks(self, srows):
        for srow in srows:
            n = len(srow)
            for j in range(n):
                srow[j].right = srow[(j + 1) % n]
                srow[j].left = srow[(j - 1 + n) % n]
            
    def createUpDownLinks(self, scols):
        for scol in scols:
            n = len(scol)
            for i in range(n):
                scol[i].down = scol[(i + 1) % n]
                scol[i].up = scol[(i - 1 + n) % n]
                scol[i].head = scol[0]
        
    def __init__(self, mat):
        
        nrows = len(mat)
        ncols = len(mat[0])
    
        srow = [[ ] for _ in range(nrows)]
        heads = [Head(j) for j in range(ncols)]        
        scol = [[head] for head in heads]

        # Head of the column heads
        self.head = Head(-1)
        heads = [self.head] + heads
            
        self.createLeftRightLinks([heads])
            
        for i in range(nrows):
            for j in range(ncols):
                if mat[i][j] == 1:
                    node = Node(i, j)
                    scol[j].append(node)
                    srow[i].append(node)

        self.createLeftRightLinks(srow)
        self.createUpDownLinks(scol)
        
    def __str__(self):
        s = ''
        byrow = [[ ] for _ in range(100)] 
        
        for col in RightIterator(self.head):
            for cell in DownIterator(col):
                byrow[cell.row].append(cell)

        for r in byrow:
            if len(r) == 0:
                break
            for c in r:
                s += str(c) + ' '
            s += '\n'
        return s

class DancingLinks:

    def __init__(self, mat):
        self.solution = [ ]
        self.smat = SparseMatrix(mat)
        
    def cover(self, col):
        col.deattach()
        for row in DownIterator(col):
            for cell in RightIterator(row):
                cell.deattach()

    def uncover(self, col):
        for row in UpIterator(col):
            for cell in LeftIterator(row):
                cell.attach()
        col.attach()    
        
    def solve(self):
        if (self.backtrack()):
            return self.solution
        return [ ]

    def backtrack(self):
        # Let's cover the first uncovered item
        col = self.smat.head.right
        # No column left
        if col == self.smat.head:
            return True
        # No set to cover this element
        if col.down == col:
            return False

        self.cover(col)
        
        for row in DownIterator(col):

            for cell in RightIterator(row):
                self.cover(cell.head)

            if self.backtrack():
                self.solution.append(row)
                return True

            for cell in LeftIterator(row):
                self.uncover(cell.head)

        self.uncover(col)
        
        return False

mat = [[0, 0, 1, 0, 1, 1, 0],
       [1, 0, 0, 1, 0, 0, 1],
       [0, 1, 1, 0, 0, 1, 0],
       [1, 0, 0, 1, 0, 0, 0],
       [0, 1, 0, 0, 0, 0, 1],
       [0, 0, 0, 1, 1, 0, 1]]

solver = DancingLinks(mat)
solution = solver.solve()
sets = [n.row for n in solution]
print 'sets ', sets
