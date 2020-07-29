MAX_SIZE_CLASS = 14
MIN_SIZE_CLASS = 8

MEM_SIZE = 1 << (MAX_SIZE_CLASS + 1)

"""
High level layout of the memory:

[SENTINELS | BLOCKS]

Layout of a block:

[FLAG | SIZE | PREV | NEXT | ACTUAL_MEMORY | SIZE ]

FLAG, SIZE, PREV, NEXT all occupy 1 unit of memory, and ACTUAL_MEMORY
occupies SIZE units. The actual size of the block is thus SIZE + 5.

FLAG is [0, 1]. 0 means available (FREE), 1 means used (USED)
"""

FREE = 0
USED = 1

METADATA_SIZE = 5
# FLAG | SIZE | PREV | NEXT
HEADER_SIZE = 4
SENTINEL_SIZE_CLASS = 3
# To mimick the structure of a block: [_flag, size, prev, next, <empty>, size]
# size = 3 so that 1<<3 = 8 has a valid block size and > space needed for metadata.
SIZE_SENTINEL = 1 << SENTINEL_SIZE_CLASS
SENTINEL_COUNT = MAX_SIZE_CLASS + 1
# One sentinel per memory size class
SENTINELS_SIZE = SIZE_SENTINEL*SENTINEL_COUNT

# Position in memory where dynamic blocks are stored
OFFSET_BLOCK = SENTINELS_SIZE
OFFSET_PREV = 2
OFFSET_NEXT = 3

class Allocator:

    def __init__(self):
        # This represents out memory. The only place we can read-write too.
        self.memory = [0]*MEM_SIZE

        block_addr = OFFSET_BLOCK

        # Represents the single full block
        self.mark_block_free(block_addr)
        self.set_block_size(block_addr, MAX_SIZE_CLASS)

        # List of doubly-linked lists to blocks of specific sizes
        for k in range(MIN_SIZE_CLASS, SENTINEL_COUNT):
            addr = self.get_sentinel_addr(k)
            # Both prev/next point to itself
            self.set_next(addr, addr)
            self.set_prev(addr, addr)

        # Add block to the largest class
        self.add_to_class_size_list(MAX_SIZE_CLASS, block_addr)

    # Find the first big-enough block that is available
    def _get_available_size_class(self, size):
        size_class = MIN_SIZE_CLASS
        while size_class < SENTINEL_COUNT and \
            (self.actual_size(size_class) < size or not self.is_available(size_class)):
            size_class += 1

        return size_class

    def alloc(self, size):
        size_class = self._get_available_size_class(size)

        if size_class == SENTINEL_COUNT:
            raise Exception('Memory is full')

        # Get first block from the list
        sentinel_addr = self.get_sentinel_addr(size_class)
        block_addr = self.get_next(sentinel_addr)

        self.remove_from_list(block_addr)

        # Keep splitting the blocks to avoid allocating too much memory
        while size_class > MIN_SIZE_CLASS and self.actual_size(size_class - 1) >= size:
            new_size_class = size_class - 1

            # Add the other half to the list
            buddy_addr = self.buddy_addr(block_addr, new_size_class)
            self.mark_block_free(buddy_addr)
            self.set_block_size(buddy_addr, new_size_class)
            self.add_to_class_size_list(new_size_class, buddy_addr)

            size_class = new_size_class

        self.mark_block_used(block_addr)
        self.set_block_size(block_addr, size_class)
        return self.get_block_memory_addr(block_addr)

    def free(self, addr):
        block_addr = self.get_block_addr_from_memory_addr(addr)
        original_size = self.get_block_size(block_addr)
        self.mark_block_free(block_addr)
        self.merge(block_addr)

    def merge(self, block_addr):
        original_size = self.get_block_size(block_addr)
        size = original_size
        while True:
            # No merge to be done
            if size == MAX_SIZE_CLASS:
                break

            buddy_addr = self.buddy_addr(block_addr, size)
            # Can't merge
            if self.is_block_used(buddy_addr):
                break

            # Buddy is not completely free (partially used)
            if self.get_block_size(buddy_addr) != size:
                break

            self.remove_from_list(buddy_addr)

            # Points to the leftmost of the pair
            # (address of the merged block)
            block_addr = min(block_addr, buddy_addr)

            size = size + 1

        # No merge happened
        if size != original_size:
            self.set_block_size(block_addr, size)

        self.add_to_class_size_list(size, block_addr)


    def buddy_addr(self, addr, size_class):
        addr = addr - OFFSET_BLOCK
        # Current address is the first buddy
        parent = 2**(size_class + 1)
        if addr % parent == 0:
            buddy_addr = addr + (1 << size_class)
        else: # Current address is the second buddy
            buddy_addr = addr - (1 << size_class)
        return buddy_addr + OFFSET_BLOCK

    # Actual size available for use
    def actual_size(self, size_class):
        return (1 << size_class) - METADATA_SIZE

    def get_block_memory_addr(self, block_addr):
        return block_addr + HEADER_SIZE

    def get_block_addr_from_memory_addr(self, addr):
        return addr - HEADER_SIZE

    def get_sentinel_addr(self, size_class):
        return size_class*SIZE_SENTINEL

    def mark_block_free(self, addr):
        self.memory[addr] = FREE

    def is_block_free(self, addr):
        return self.memory[addr] == FREE

    def mark_block_used(self, addr):
        self.memory[addr] = USED

    def is_block_used(self, addr):
        return self.memory[addr] == USED

    def set_block_size(self, addr, size):
        self.memory[addr + 1] = size

    def get_block_size(self, addr):
        return self.memory[addr + 1]

    def set_prev(self, addr, dest_addr):
        self.memory[addr + OFFSET_PREV] = dest_addr

    def get_prev(self, addr):
        return self.memory[addr + OFFSET_PREV]

    def set_next(self, addr, dest_addr):
        self.memory[addr + OFFSET_NEXT] = dest_addr

    def get_next(self, addr):
        return self.memory[addr + OFFSET_NEXT]

    def is_available(self, size_class):
        addr = self.get_sentinel_addr(size_class)
        is_empty = self.get_next(addr) == addr
        return not is_empty

    # Insert at the beginning of a linked list
    def add_to_class_size_list(self, size_class, node_addr):
        list_addr = self.get_sentinel_addr(size_class)
        next_node_addr = self.get_next(list_addr)
        self.set_next(list_addr, node_addr)
        self.set_prev(node_addr, list_addr)
        self.set_prev(next_node_addr, node_addr)
        self.set_next(node_addr, next_node_addr)

    # Remove the block from the list it's at. Its own
    # pointers become undefined
    def remove_from_list(self, node_addr):
        next_node_addr = self.get_next(node_addr)
        prev_node_addr = self.get_prev(node_addr)
        self.set_next(prev_node_addr, next_node_addr)
        self.set_prev(next_node_addr, prev_node_addr)

    # For debugging / testing
    def get_histogram(self):
        histo = {}
        for k in range(MIN_SIZE_CLASS, SENTINEL_COUNT):
            block_count = 0
            addr = self.get_sentinel_addr(k)
            block_addr = self.get_next(addr)
            while block_addr != addr:
                block_count += 1
                new_block_addr = self.get_next(block_addr)
                assert new_block_addr != block_addr, f"Corrupted list for size {k}"
                block_addr = new_block_addr

            if block_count > 0:
                histo[k] = block_count
        return histo
