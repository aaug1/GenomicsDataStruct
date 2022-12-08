import sys
import math
from collections import deque



def convert_to_int(seq):
    converted = []
    arr = ["A", "C", "G", "T"]
    for c in seq:
        converted.append(str(arr.index(c)))
    return int(''.join(converted), 4)

class CountMin:
    def __init__(self, epsilon, delta):

        self.w = None
        self.d = None
        self.sketch = [ [ 0 for i in range(self.w) ] for j in range(self.d) ]

        self.p = 2 ** 61 - 1
        self.a = []
        self.b = []
        for i in range(self.d):
            self.a.append(2 * (i + 1) + 1)
            self.b.append(i + 1)
    
    def hash(self, i, index):
        return (index * self.a[i] + self.b[i]) % self.p % self.w

    def store(self, index, num):
        # TODO
        return

    def check(self, index):
        # TODO
        return 0

x = CountMin(0.25, 0.25)


# Store sequence of keys
x.store(convert_to_int("AA"), 1)
x.store(convert_to_int("AC"), 2)
x.store(convert_to_int("AG"), 3)
x.store(convert_to_int("AT"), 4)
x.store(convert_to_int("CA"), 5)
x.store(convert_to_int("CC"), 6)
x.store(convert_to_int("CG"), 7)
x.store(convert_to_int("CT"), 8)

# Check those keys probably exist
print('Check presence for those in')
x.check(convert_to_int("AA"))
x.check(convert_to_int("AC"))
x.check(convert_to_int("AG"))
x.check(convert_to_int("AT"))
x.check(convert_to_int("CA"))
x.check(convert_to_int("CC"))
x.check(convert_to_int("CG"))
x.check(convert_to_int("CT"))

# # Check for keys that likely do not exist
print('Check presence for those not in')
x.check(convert_to_int("GA"))
x.check(convert_to_int("GC"))
x.check(convert_to_int("GG"))
x.check(convert_to_int("TT"))
x.check(convert_to_int("TA"))
x.check(convert_to_int("TC"))
x.check(convert_to_int("TG"))
x.check(convert_to_int("TT"))