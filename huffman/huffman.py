#!/usr/bin/env python3

from simple_queue import Queue
from bitarray import bitarray

class Node:
    def __init__(self, val, symbol, left, right):
        self.val = val
        self.symbol = symbol
        self.left = left
        self.right = right

    @staticmethod
    def combine(left, right):
        return Node(left.val + right.val, None, left, right)

    @staticmethod
    def symbol(val, symbol):
        return Node(val, symbol, None, None)

    def less(self, other):
        return self.val < other.val


def less(elem1, elem2):
    if elem1 is None and elem2 is None:
        raise Exception('Either elements must be non null')
    if elem1 is None:
        return False
    if elem2 is None:
        return True
    return elem1.less(elem2)

def sort_map_by_value(m):
    return {
        k: v for k, v in sorted(m.items(), key=lambda i: i[1])
    }

def build_tree(frequency_map):
    frequency_map = sort_map_by_value(frequency_map)

    nodes = []
    for [symbol, f] in frequency_map.items():
        node = Node.symbol(f, symbol)
        nodes.append(node)

    q1 = Queue(nodes)
    q2 = Queue()

    def get_min(q1, q2):
        if less(q1.front(), q2.front()):
            return q1.pop()
        else:
            return q2.pop()

    while q1.len() + q2.len() >= 2:

        x = get_min(q1, q2)
        y = get_min(q1, q2)
        s = Node.combine(x, y)
        q2.push(s)


    return q2.front()

def build_lookup(tree):
    def traverse(node, path, lookup):
        if node.symbol:
            # Clone, reverse
            lookup[node.symbol] = path[::]
        else:
            # To be efficient, update path in place...
            path.append(0)
            traverse(node.left, path, lookup)

            path[-1] = 1
            traverse(node.right, path, lookup)

            # ...but restore it once done
            path.pop()

    lookup = {}
    traverse(tree, bitarray(), lookup)
    return lookup

def encode(text, tree):
    lookup = build_lookup(tree)
    encoded = bitarray()
    for c in text:
        code = lookup[c]
        encoded.extend(code)
    return encoded

def decode(encoded, tree):
    node = tree
    text = ''
    for bit in encoded:
        if bit is False:
            node = node.left
        else:
            node = node.right

        if node.symbol is not None:
            text += node.symbol
            node = tree

    return text

def compute_huffman_entropy(frequency_map):
    tree = build_tree(frequency_map)
    lookup = build_lookup(tree)

    norm_factor = sum(frequency_map.values())

    entropy = 0.0
    for [symbol, f] in frequency_map.items():
        code_len = len(lookup[symbol])
        norm_f = f / norm_factor
        entropy += norm_f * code_len
    return entropy
