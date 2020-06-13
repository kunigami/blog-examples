class Queue:
    def __init__(self, initial=None):
        if initial is None:
            initial = []
        self.queue = initial
        self.head = 0

    def front(self):
        if self.is_empty():
            return None
        return self.queue[self.head]

    def is_empty(self):
        return self.len() == 0

    def pop(self):
        if self.is_empty():
            return None
        val = self.front()
        self.head += 1
        return val

    def push(self, elem):
        self.queue.append(elem)

    def len(self):
        return len(self.queue) - self.head
