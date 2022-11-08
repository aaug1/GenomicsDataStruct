import hashlib
import math
import random

# https://www.pdl.cmu.edu/PDL-FTP/FS/cuckoo-conext2014.pdf
# https://medium.com/@meeusdylan/implementing-a-cuckoo-filter-in-go-147a5f1f7a9


class CuckooFilter:
  # n = len(items), fp = false positive rate
    def __init__(self, n: int, fp: float):
        self.b = 4  # entries per bucket
        self.max_kicks = 200  # number of kicks to try before giving up and declaring cycle
        # How long a fingerprint in bytes
        self.f = self.fingerprintLength(self.b, fp)
        numBits = int((n / self.f) * 8)
        self.m = self.nextPower(numBits)  # buckets
        self.buckets = [[None]*self.b for i in range(self.m)]
        self.n = n  # filter capacity (rename cap?)

    def insert(self, input: str):
        i1, i2, f = self.hashes(input)
        capped_i1 = i1 % self.m
        capped_i2 = i2 % self.m
        # The modulo self.m is to cap the hash so it can be used as an actual index
        for e1_index in range(len(self.buckets[capped_i1])):
            if self.buckets[capped_i1][e1_index] is None:
                self.buckets[capped_i1][e1_index] = f
                return

        for e2_index in range(len(self.buckets[capped_i2])):
            if self.buckets[capped_i2][e2_index] is None:
                self.buckets[capped_i2][e2_index] = f
                return
        # reached here means both places were full so must relocate existing items
        self.relocate(i1, i2, f)

    def lookup(self, input: str):
        i1, i2, f = self.hashes(input)
        capped_i1 = i1 % self.m
        capped_i2 = i2 % self.m
        return f in self.buckets[capped_i1] or f in self.buckets[capped_i2]

    def relocate(self, i1, i2, f):
        i = random.choice([i1, i2])
        for n in range(self.max_kicks):
            bucket_index = i % self.m
            # randomly select an entry e from bucket[i];
            entry_index = random.randrange(self.b)
            kicked_f = self.buckets[bucket_index][entry_index]
            self.buckets[bucket_index][entry_index] = f
            hash_f = int.from_bytes(self.sha_hash(kicked_f), "big")
            i = i ^ hash_f
            capped_i = i % self.m
            for entry_i in range(len(self.buckets[capped_i])):
                if self.buckets[capped_i][entry_i] is None:
                    self.buckets[capped_i][entry_i] = kicked_f
                    return
        raise Exception("Failue: Hashtable is full")

    def hashes(self, val: str):
        h = self.sha_hash(bytes(val, 'utf-8'))
        # We want to store the finger print, not the value
        fingerprint = h[0: self.f]
        i1 = int.from_bytes(h, "big")
        hash_f = int.from_bytes(self.sha_hash(fingerprint), "big")
        # xor because I no longer need to rely on the value string to calculate a second hash in collisions.
        # I can get an alternate by xoring i1 and hash of a finger print to get the 2nd index later on
        i2 = i1 ^ hash_f
        # returning the really big indicies and the fingerprint to store
        # the modulo self.m is to cap the i1 nad i2 to be indicies of the actual buckets array
        return i1, i2, fingerprint

    # val must already be in bytes
    def sha_hash(self, byte_val):
        hashObj = hashlib.sha1(byte_val)
        return hashObj.digest()

    # returns the length of finger print in bytes
    def fingerprintLength(self, b: int, e: float):
        f = math.ceil(math.log(2 * float(b) / e))
        f /= 8  # divide by 8 to get the number of bytes
        if f < 1:
            return 1
        return f  # We want to limit the bytes to at least 1.

    # https://cs.stackexchange.com/questions/81876/cuckoo-filters-for-non-powers-of-2
    # So apparently the storage in cuckoo should be a power of 2 if you want 95% load factor
    # Mark I need to look at this again
    def nextPower(self, i: int):
        i -= 1
        i |= i >> 1
        i |= i >> 2
        i |= i >> 4
        i |= i >> 8
        i |= i >> 16
        i |= i >> 32
        i += 1
        return i


p1 = CuckooFilter(3, 0.1)

p1.insert('qojngwdf112323')
p1.insert('somethiqweng')
print(p1.lookup('somethiqweng'))
# p1.insert('1')
# p1.insert('2')
# print(p1.buckets)
