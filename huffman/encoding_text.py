from huffman import Node, build_tree, decode, encode, compute_huffman_entropy
from entropy import compute_entropy

if __name__ == '__main__':

    frequency_map = {}

    filename = 'pride-and-prejudice.txt'
    i = 0
    text = ''
    words = []
    with open(filename, "r") as file:
        for line in file:
            for c in line:
                if c not in frequency_map:
                    frequency_map[c] = 0
                frequency_map[c] += 1
            text += line
            words += [w.strip(' \n.,”“') for w in line.split()]

    min_entropy = compute_entropy(frequency_map.values())
    print('Minimum entropy', min_entropy)

    huffman_entropy = compute_huffman_entropy(frequency_map)
    print('Huffman entropy', huffman_entropy)

    tree = build_tree(frequency_map)
    encoded_text = encode(text, tree)
    print('Length of raw text: {} bytes'.format(len(text)))
    print('Length of encoded text: {} bytes'.format(len(encoded_text)/8))
    print('Compression rate: {}'.format(len(text)*8/len(encoded_text)))

    print('= Word-based =')
    text_length = 0

    frequency_map = {}
    for w in words:
        text_length += len(w)
        if w not in frequency_map:
            frequency_map[w] = 0
        frequency_map[w] += 1
    avg_word_size = text_length / len(words)

    min_entropy = compute_entropy(frequency_map.values())
    print('Minimum entropy', min_entropy / avg_word_size)
    huffman_entropy = compute_huffman_entropy(frequency_map)
    print('Huffman entropy', huffman_entropy / avg_word_size)

    tree = build_tree(frequency_map)
    encoded_text = encode(words, tree)
    print('Length of raw text: {} bytes'.format(text_length))
    print('Length of encoded text: {} bytes'.format(len(encoded_text)/8))
    print('Compression rate: {}'.format(text_length*8/len(encoded_text)))
