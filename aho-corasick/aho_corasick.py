from queue import Queue


class Node:
    def __init__(self):
        self.goto = {}
        self.fail = {}
        # if set, represents a keyword
        self.entry = None
        # links to the next suffix that is a keyword
        self.output = None
        # longest proper suffix that is another node
        self.suffix = None

    def get_matches(self):
        matches = []
        output = self
        while output is not None:
            if (output.entry is not None):
                matches.append(output.entry)
            output = output.output
        return matches


def get_letters(entries):
    alphabet = set()
    for entry in entries:
        for c in entry:
            alphabet.add(c)

    return alphabet


def insert_trie(trie, entry):
    node = trie
    for c in entry:
        if c not in node.goto:
            node.goto[c] = Node()
        node = node.goto[c]
    node.entry = entry


def build_structure(entries):
    trie = Node()
    trie.suffix = trie

    for entry in entries:
        insert_trie(trie, entry)

    queue = Queue()
    queue.put(trie)

    alphabet = get_letters(entries)

    while not queue.empty():
        node = queue.get()

        for a in alphabet:

            suffix = node.suffix
            while suffix is not trie and a not in suffix.goto:
                suffix = suffix.suffix

            jump_node = trie
            if a in suffix.goto:
                jump_node = suffix.goto[a]

            if a not in node.goto:
                node.fail[a] = jump_node
                continue

            child = node.goto[a]

            if jump_node is child:  # cannot jump to itself
                jump_node = trie
            child.suffix = jump_node

            if jump_node.entry is not None:
                child.output = jump_node
            else:
                child.output = jump_node.output

            queue.put(child)

    return trie


def search(text, entries):
    lookup = build_structure(entries)
    # return
    node = lookup
    match_pairs = []
    for i, c in enumerate(text):
        if c in node.goto:
            node = node.goto[c]
        elif c in node.fail:
            node = node.fail[c]
        else:
            node = lookup
        matches = node.get_matches()
        if len(matches) > 0:
            for match in matches:
                match_pairs.append((i - len(match) + 1, i + 1))
    return match_pairs
