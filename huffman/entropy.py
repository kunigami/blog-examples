from math import log

def log2(x):
    return log(x)/log(2)

def compute_entropy(fs):
    tot = 1.0*sum(fs)
    entropy = 0
    for f in fs:
        norm_f = f/tot
        entropy += (-norm_f*log2(norm_f))
    return entropy
