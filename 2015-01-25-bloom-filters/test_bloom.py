from bloom import BloomFilter
import random

random.seed(0)

def bloom_filter_run(n, m, k=None):
    keys = range(n)
    # Random sampling without replacement
    random.shuffle(keys)
    probs = []
    filter = BloomFilter(m, n, k)
    inserted = [False]*(n)

    for cnt, entry in enumerate(keys):
        filter.insert(str(entry))

        inserted[entry] = True
        false_positives, total = 0, 0
        # Compute false positives
        for probe in range(n):
            if not inserted[probe]:
                exists = filter.query(probe)
                if exists:
                    false_positives += 1
                total += 1
        if total != 0:
            prob = false_positives*1.0 / total
            probs.append(prob)
    return probs

n = 250

def bitarray_size_experiment():
    all_probs = {}
    for m in [100, 250, 500, 1000]:
        probs = bloom_filter_run(n, m)
        all_probs[m] = probs

    print 'n, prob, m'
    for m in all_probs:
        for i, p in enumerate(all_probs[m]):
            if p is not None:
                print '{}, {}, m={}'.format(i, p, m)

def number_of_hash_functions_experiment():
    all_probs = {}
    m = 1000
    for k in [1, 5, 10, 50]:
        probs = bloom_filter_run(n, m, k)
        all_probs[k] = probs

    print 'n, prob, k'
    for k in all_probs:
        for i, p in enumerate(all_probs[k]):
            klabel = "lg(2)" if k is None else k
            if p is not None:
                print '{}, {}, k={}'.format(i, p, klabel)


#bitarray_size_experiment()
number_of_hash_functions_experiment()
