class QueueList:
    left = []
    right = []

    def push(self, elem):
        if not self.left:
            self.left = [elem]
        else:
            self.right.append(elem)
        return self

    def pop(self):
        if not self.left:
            raise RuntimeError('Empty queue')
        elem = self.left.pop()
        if not self.left:
            self.left = self.right
            self.left.reverse()
            self.right = []
        return elem

    def isEmpty(self):
        return len(self.left) == 0

    def __str__(self):
        reversedLeft = list(self.left)
        reversedLeft.reverse()
        return ', '.join(
            map(str, reversedLeft + self.right)
        )
