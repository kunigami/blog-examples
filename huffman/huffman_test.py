import unittest

from huffman import Node, build_tree, build_lookup, decode, encode, compute_huffman_entropy
from entropy import compute_entropy

class HuffmanTest(unittest.TestCase):

    def test_combining_nodes(self):
        c1 = Node.symbol(0.4, 'a')
        c2 = Node.symbol(0.6, 'b')
        p = Node.combine(c1, c2)

        self.assertEqual(p.left, c1)
        self.assertEqual(p.right, c2)
        self.assertEqual(p.val, 1.0)
        self.assertEqual(p.symbol, None)


    def test_building_encoding_wikipedia(self):
        frequency_map = get_wikipedia_input()
        tree = build_tree(frequency_map)
        lookup = build_lookup(tree)
        # Human readable
        lookup_readable = {k: bits.to01() for k, bits in lookup.items()}
        self.assertEqual(
            lookup_readable,
            {'a': '010', 'b': '011', 'c': '11', 'd': '00', 'e': '10'}
        )

    def test_building_encoding_for_degenerated(self):
        frequency_map = get_degenerated_input()
        tree = build_tree(frequency_map)
        lookup = build_lookup(tree)
        # Human readable
        lookup_readable = {k: bits.to01() for k, bits in lookup.items()}
        self.assertEqual(
            lookup_readable,
            {'a': '0000', 'b': '0001', 'c': '001', 'd': '01', 'e': '1'}
        )

    def test_building_encoding_for_uniform(self):
        frequency_map = get_uniform_input()
        tree = build_tree(frequency_map)
        lookup = build_lookup(tree)
        # Human readable
        lookup_readable = {k: bits.to01() for k, bits in lookup.items()}
        self.assertEqual(
            lookup_readable,
            {'a': '110', 'b': '111', 'c': '00', 'd': '01', 'e': '10'}
        )

    def test_encoding(self):
        frequency_map = get_wikipedia_input()
        tree = build_tree(frequency_map)
        encoded = encode('adeaddadcededabadbabeabeadedabacabed', tree)
        self.assertEqual(
            encoded.to01(),
            '01000100100000010001110001000010011010000110100111001001110010001000010011010110100111000'
        )

    def test_decoding(self):
        frequency_map = get_wikipedia_input()
        tree = build_tree(frequency_map)
        samples = [
            'a',
            'abc',
            'adeaddadcededabadbabeabeadedabacabed'
        ]
        for text in samples:
            encoded = encode(text, tree)
            decoded = decode(encoded, tree)
            self.assertEqual(text, decoded)

    def test_decoding_real_world(self):
        frequency_map = get_real_world_input()
        tree = build_tree(frequency_map)
        text = get_real_world_text()
        encoded = encode(text, tree)
        decoded = decode(encoded, tree)
        self.assertEqual(text, decoded)

    def test_entropy(self):
        frequency_maps = [
            get_wikipedia_input(),
            get_degenerated_input(),
            get_uniform_input(),
            get_real_world_input()
        ]

        for frequency_map in frequency_maps:
            huffman_entropy = compute_huffman_entropy(frequency_map)
            min_entropy = compute_entropy(frequency_map.values())
            self.assertTrue(huffman_entropy >= min_entropy)
            self.assertTrue(huffman_entropy <= min_entropy + 1)

def get_wikipedia_input():
    return {'a': 0.10, 'b': 0.15, 'c': 0.30, 'd': 0.16, 'e': 0.29}

def get_degenerated_input():
    return {'a': 1, 'b': 2, 'c': 4, 'd': 8, 'e': 16}

def get_uniform_input():
    return {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1}

def get_real_world_input():
    frequency_map = {}
    text = get_real_world_text()
    for c in text:
        if c not in frequency_map:
            frequency_map[c] = 0
        frequency_map[c] += 1
    return frequency_map

def get_real_world_text():
    text = ''
    filename = 'pride-and-prejudice.txt'
    with open(filename, "r") as file:
        for line in file:
            text += line
    return text


if __name__ == '__main__':

    unittest.main()
