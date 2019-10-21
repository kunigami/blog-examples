def naive_search(Q, T):

    tlen = len(T)
    qlen = len(Q)

    matches = []
    for i, _ in enumerate(T):
        match = 0
        while match < qlen and \
              i + match < tlen and \
              Q[match] == T[i + match]:
            match += 1

        if match == qlen:
            matches.append(i)
    return matches

def precompute_lsp_naive(Q):
    qlen = len(Q)
    lsp = [0]*qlen

    i = 1
    while i < qlen :

        j = 0
        while (i + j < qlen and Q[j] == Q[j + i]):
            lsp[i + j] = max(lsp[i + j], j + 1)
            j += 1

        i += 1
    return lsp

def precompute_lsp(Q):

    qlen = len(Q)

    lsp = [0]*qlen

    i = 1
    j = 0
    while i < qlen:
        if Q[i] == Q[j]:
            j += 1
            i += 1
            lsp[i - 1] = j
        else:
            j = lsp[j - 1]
            if j == 0:
                i += 1

    return lsp

def kmp_generic(Q, T, yield_indices):

    lsp = precompute_lsp(Q)

    i = 0
    j = 0

    qlen = len(Q)
    tlen = len(T)

    while i < tlen:

        if j < qlen and Q[j] == T[i]:
            j += 1
            i += 1
        elif j > 0:
            j = lsp[j - 1]
        else:
            i += 1

        yield_indices(i, j)


def kmp_all_matches(Q, T):
    matches = []
    qlen = len(Q)
    def match_accumulator(i, j):
        if j == qlen:
            matches.append(i - j)
    kmp(Q, T, match_accumulator)
    return matches

def longest_suffix_prefix(suffix, prefix):
    slen = len(suffix)
    max_match = [None]
    def max_matcher(i, j):
        if max_match[0] is None and i == slen:
            max_match[0] = j

    # Search prefix in suffix
    kmp(prefix, suffix, max_matcher)

    return 0 if max_match[0] is None else max_match[0]

def longest_suffix_prefix_naive(suffix, prefix):
    minlen = min(len(prefix), len(suffix))
    max_match = 0
    for match_len in range(1, minlen + 1):
        if prefix[:match_len] == suffix[-match_len:]:
            max_match = match_len
    return max_match

f = open('test_cases.txt', 'r')
for line in f:

    line = line.strip(' ')
    # Skip metadata
    if len(line) == 0 or line.startswith('#'):
        continue

    (needle, haystack) = line.split()

    # Test KMP
    matches = kmp_all_matches(needle, haystack)
    matches_naive = naive_search(needle, haystack)
    assert matches == matches_naive

    # Test LSP function
    lsp = precompute_lsp(needle)
    reference_lsp = precompute_lsp_naive(needle)
    assert lsp == reference_lsp

print 'Success!'

f = open('lsp_tests.txt', 'r')
for line in f:

    (suffix, prefix) = line.split()
    print suffix, prefix
    max_match = longest_suffix_prefix(suffix, prefix)
    max_match_naive = longest_suffix_prefix_naive(suffix, prefix)
    assert max_match == max_match_naive, \
           "{} should match {}".format(max_match, max_match_naive)

