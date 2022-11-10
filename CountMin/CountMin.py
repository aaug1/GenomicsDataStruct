import sys
import math
from collections import deque

def convert_to_int(seq):
    converted = []
    arr = ["A", "C", "G", "T"]
    for c in seq:
        converted.append(str(arr.index(c)))
    return int(''.join(converted), 4)

file_name = sys.argv[1]

k = int(sys.argv[2])

epsilon = float(sys.argv[3])

delta = float(sys.argv[4])

w = math.ceil(math.e / epsilon)
d = math.ceil(math.log(1 / delta))

sketch = [ [ 0 for i in range(w) ] for j in range(d) ]

p = 2 ** 61 - 1
a = []
b = []
for i in range(d):
    a.append(2 * i + 1)
    b.append(i + 1)

kmers = 0
with open(file_name) as f:
    f.readline()
    queue = deque(maxlen=k)
    while True:
        c = f.read(1)
        if not c:
            break
        if c not in 'ACGT':
            continue
        queue.append(c)
        kmer = ''.join(queue)
        num = convert_to_int(kmer)
        if len(kmer) != k: continue
        for i in range(d):
            idx = (num * a[i] + b[i]) % p % w
            sketch[i][idx] += 1
        kmers += 1
print(sketch)
print(kmers)
while True:
    try:
        line = input()
        if len(line) != k:
            print("must be length " + str(k))
            continue
        minimum = float("inf")
        num = convert_to_int(line)
        for i in range(d):
            idx = (num * a[i] + b[i]) % p % w
            minimum = min(minimum, sketch[i][idx])
        if (minimum > 0):
            print("Might be there: " + str(minimum))
        else:
            print("Not there")
    except EOFError:
        break
