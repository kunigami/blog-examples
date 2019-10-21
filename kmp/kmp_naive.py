T = 'ababacababa'
Q = 'baca'

def substr(Q, T):

    tlen = len(T)
    qlen = len(Q)

    for i, _ in enumerate(T):
        match = 0
        while match < qlen and \
              i + match < tlen and \
              Q[match] == T[i + match]:
            match += 1

        if match == qlen:
            print 'found substring in position', i

substr(Q, T)

