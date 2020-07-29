MAX_SIZE_CLASS = 14
MIN_SIZE_CLASS = 8

MEM_SIZE = 1 << (MAX_SIZE_CLASS + 1)

"""
High level layout of the memory:

[SENTINELS | BLOCKS]

Layout of a block:

[FLAG | SIZE | PREV | NEXT | ACTUAL_MEMORY]

FLAG, SIZE, PREV, NEXT all occupy 1 unit of memory. The size of the block is 2^SIZE,
so ACTUAL_MEMORY is 2^SIZE - 4 units.

FLAG is [0, 1]. 0 means available (FREE), 1 means used (USED)
"""

FREE = 0
USED = 1

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

class Allocator:

    def __init__(self):
        # This represents out memory. The only place we can read-write too.
        self.memory = Memory(MEM_SIZE)
        free_blocks = self.get_free_blocks()

        block = self.get_block_at(OFFSET_BLOCK)

        # Represents the single full block
        block.set_free()
        block.set_size(free_blocks.get_larget_class_size())

        free_blocks.clear()
        free_blocks.add_block(block)

    def get_free_blocks(self):
        return ListsOfBlocks(MIN_SIZE_CLASS, MAX_SIZE_CLASS, self.memory)

    def alloc(self, size):
        free_blocks = self.get_free_blocks()
        size_class = free_blocks.get_fittest_size_class(size)

        if size_class == SENTINEL_COUNT:
            raise Exception('Memory is full')

        # Get first block from the list
        head = free_blocks.get_list_head(size_class)
        block = head.get_next()

        block.remove_from_list()

        # Keep splitting the blocks to avoid allocating too much memory
        while size_class > MIN_SIZE_CLASS and Block.get_actual_size(size_class - 1) >= size:
            new_size_class = size_class - 1

            # Add the other half to the list
            buddy = self.get_buddy(block, new_size_class)
            buddy.set_free()
            buddy.set_size(new_size_class)
            free_blocks.add_block(buddy)

            size_class = new_size_class

        block.set_used()
        block.set_size(size_class)
        return block.get_user_addr()

    def get_block_at(self, addr):
        return Block(addr, self.memory)

    def free(self, user_addr):
        block = Block.from_user_addr(user_addr, self.memory)
        block.set_free()
        self.merge(block)

    def merge(self, block):
        free_blocks = self.get_free_blocks()

        original_size = block.get_size()
        size = original_size
        while True:
            # No merge to be done
            if size == MAX_SIZE_CLASS:
                break

            buddy = self.get_buddy(block, size)
            # Can't merge
            if buddy.is_used():
                break

            # Buddy is not completely free (partially used)
            if buddy.get_size() != size:
                break

            buddy.remove_from_list()

            # Points to the leftmost of the pair
            # (address of the merged block)
            if (block.addr > buddy.addr):
                block = buddy

            size = size + 1

        # No merge happened
        if size != original_size:
            block.set_size(size)

        free_blocks.add_block(block)

    def buddy_addr(self, addr, size_class):
        addr = addr - OFFSET_BLOCK
        # Current address is the first buddy
        parent = 2**(size_class + 1)
        if addr % parent == 0:
            buddy_addr = addr + (1 << size_class)
        else: # Current address is the second buddy
            buddy_addr = addr - (1 << size_class)
        return buddy_addr + OFFSET_BLOCK

    def get_buddy(self, block, size_class):
        buddy_addr = self.buddy_addr(block.addr, size_class)
        return Block(buddy_addr, self.memory)

    def get_histogram(self):
        return self.get_free_blocks().get_histogram()

class ListsOfBlocks:

    def __init__(self, lower_bound_size, upper_bound_size, memory):
        self.lower_bound_size = lower_bound_size
        self.upper_bound_size = upper_bound_size
        self.memory = memory

    def clear(self):
        for k in range(self.lower_bound_size, self.upper_bound_size + 1):
            head = self.get_list_head(k)
            # Both prev/next point to itself
            head.set_next(head)
            head.set_prev(head)

    def get_larget_class_size(self):
        return self.upper_bound_size

    def add_block(self, block):
        size_class = block.get_size()
        self.get_list_head(size_class).insert_after(block)

    def get_list_head(self, size_class):
        addr = size_class*SIZE_SENTINEL
        return Block(addr, self.memory)

    def is_empty(self, size_class):
        head = self.get_list_head(size_class)
        return head.get_next().addr == head.addr

    def get_fittest_size_class(self, size):
        size_class = self.lower_bound_size
        while size_class <= self.upper_bound_size and \
            (Block.get_actual_size(size_class) < size or self.is_empty(size_class)):
            size_class += 1
        return size_class

    # For debugging / testing
    def get_histogram(self):
        histo = {}
        for k in range(self.lower_bound_size, self.upper_bound_size + 1):
            block_count = 0
            head = self.get_list_head(k)
            block = head.get_next()
            while not block.equal(head):
                block_count += 1
                new_block = block.get_next()
                assert not block.equal(new_block), f"Corrupted list for size {k}"
                block = new_block

            if block_count > 0:
                histo[k] = block_count
        return histo

# Offsets within a block
OFFSET_PREV = 2
OFFSET_NEXT = 3

class Block:

    def __init__(self, addr, memory):
        self.memory = memory
        self.addr = addr

    @staticmethod
    def from_user_addr(user_addr, memory):
        return Block(user_addr - HEADER_SIZE, memory)

    @staticmethod
    def get_actual_size(size_class):
        return (1 << size_class) - HEADER_SIZE

    def get_user_addr(self):
        return self.addr + HEADER_SIZE

    def set_used(self):
        self.memory.write_bool(self.addr, USED)

    def is_used(self):
        return self.memory.get_bool(self.addr) == USED

    def set_free(self):
        self.memory.write_bool(self.addr, FREE)

    def set_size(self, size):
        self.memory.write_i16(self.addr + 1, size)

    def get_size(self):
        return self.memory.get_i16(self.addr + 1)

    def set_prev(self, block):
        self.memory.write_i16(self.addr + OFFSET_PREV, block.addr)

    def get_prev(self):
        addr = self.memory.get_i16(self.addr + OFFSET_PREV)
        return Block(addr, self.memory)

    def set_next(self, block):
        self.memory.write_i16(self.addr + OFFSET_NEXT, block.addr)

    def get_next(self):
        addr = self.memory.get_i16(self.addr + OFFSET_NEXT)
        return Block(addr, self.memory)

    def equal(self, other):
        return self.addr == other.addr

    def insert_after(self, block):
        next_block = self.get_next()
        self.set_next(block)
        block.set_prev(self)
        next_block.set_prev(block)
        block.set_next(next_block)

    # Remove the block from the list it's at. Its own
    # pointers become undefined
    def remove_from_list(self):
        next_block = self.get_next()
        prev_block = self.get_prev()
        prev_block.set_next(next_block)
        next_block.set_prev(prev_block)

class Memory:

    def __init__(self, size):
        self.memory = [0]*size

    def write_bool(self, addr, val):
        self.memory[addr] = val

    def get_bool(self, addr):
        return self.memory[addr]

    def write_i16(self, addr, val):
        self.memory[addr] = val

    def get_i16(self, addr):
        return self.memory[addr]
