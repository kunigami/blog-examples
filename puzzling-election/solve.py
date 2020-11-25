import csv

filename = "2016-election.csv"

def to_num(s):
    return int(s.replace(',', ''))

def read_raw_data():
    with open(filename, "r") as csvfile:

        reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
        # ys = [line for line in file.readLines()]
        # print(ys)
        data = []

        first = True
        for line in reader:
            [state, votes, evotes] = line
            if first:
                first = False
            else:
                data.append([state, to_num(votes), to_num(evotes)])
    return data

def get_items(data):
    items = []
    for row in data:
        items.append({
            'id': row[0],
            'c': row[1] // 2 + 1,
            'w': row[2]
        })
    return items

def solve_knapsack(items, W):
    k = [-1]*(W + 1)
    # Empty set
    k[0] = 0
    # ks[i][w] represents the best possible knapsack value using
    # only the first i-1 items and with size w.
    ks = [k]

    for item in items:
        next_k = k.copy()
        for w in range(len(k)):
            next_w = w + item['w']
            if next_w > W:
                break

            if k[w] < 0:
                continue

            next_c = k[w] + item['c']
            if k[next_w] == -1 or k[next_w] < next_c:
                next_k[next_w] = next_c

        k = next_k
        ks.append(k)

    # Find the best size
    max_w = W
    while ks[-1][max_w] == -1:
        max_w -= 1

    # Backtrack to find which items were used
    picked = []
    curr_w = max_w
    # idx refers to the idx-1-th item, because best's first
    # element (position 0) is a sentinel.
    for idx in reversed(range(len(ks))):
        if ks[idx][curr_w] > ks[idx - 1][curr_w]:
            picked.append(idx - 1)
            curr_w -= items[idx - 1]['w']

    # Make sure the solution we picked correspond to the value we obtained.
    assert ks[-1][max_w] == sum([items[idx]['c'] for idx in picked])

    return picked


def solve_inverse_knapsack(items, W):
    total_weight = sum([item['w'] for item in items])
    solution = solve_knapsack(items, total_weight - W)
    solution_lookup = set(solution)
    # the complement of items in solution
    return [i for i in range(len(items)) if i not in solution_lookup]


data = read_raw_data()
items = get_items(data)
print(items)
picked_idx = solve_inverse_knapsack(items, 270)

states = [items[idx]['id'] for idx in picked_idx]
print('States where A wins:', states)

eva = sum([items[idx]['w'] for idx in picked_idx])
total_weight = sum([item['w'] for item in items])
evb = total_weight - eva
print('Total electoral votes:', total_weight)
print('Electoral votes for A:', eva)
print('Electoral votes for B:', evb)

pva = sum([items[idx]['c'] for idx in picked_idx])
total_votes = sum([row[1] for row in data])
pvb = total_votes - pva

print('Total popular votes:', total_votes)
print('Popular votes for A:', pva)
print('Popular votes for B:', pvb)
print('Difference of B and A:', pvb - pva)
