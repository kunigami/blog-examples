from pyhash import murmur3_x64_128

hasher = murmur3_x64_128()

def single():
    N = 10000
    print 'i, h_i'
    for i in range(N):
        h = hasher(str(i)) % N
        print "{}, {}".format(i, h)

def family():
    N = 1000
    print 'i, h_i, class'
    for i in range(N):
        h128 = hasher(str(i))
        h64l = h128 & ((1L << 64) - 1)
        h64u = h128 >> 64

        for j in range(5):
            h = (h64l + j*h64u) % N
            print "{}, {}, {}".format(i, h, j)

def family_pairwise():

    print 'h_i, h_j, class'
    for i in range(N):
        h128 = hasher(str(i))
        h64l = h128 & ((1L << 64) - 1)
        h64u = h128 >> 64

        h = [0]*5
        for j in range(5):
            h[j] = ((j+1)*h64u) % N

        for j in range(5):
            for k in range(5):
                print "{}, {}, h{}_{}".format(h[j], h[k], j, k)
