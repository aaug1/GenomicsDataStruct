import hashlib
import math
import random


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
        """Attempt to insert the input into a place in the filter using the capped indices and the fingerprint f"""
        # TODO

        """If there is no available space, attempt to relocate"""
        self.relocate(i1, i2, f)

    def relocate(self, i1, i2, f):
        """Pick a random item in one of the full indices and calculate the alternate index and attempt to place it there"""
        """Keep trying until all insertions work or there have been too many cycles"""
        # TODO

        """If there have been too many cycles throw that the insertion failed"""
        raise Exception("Failue: Hashtable is full")

    def lookup(self, input: str):
        i1, i2, f = self.hashes(input)
        capped_i1 = i1 % self.m
        capped_i2 = i2 % self.m

        """Attempt to find the input in the filter, return true if it was found, false if not"""
        # TODO
        return False

    def delete(self, input: str):
        i1, i2, f = self.hashes(input)
        capped_i1 = i1 % self.m
        capped_i2 = i2 % self.m

        """Attempt to delete an object from the filter. Return True if successful"""
        # TODO

        return False

    def hashes(self, val: str):
        byte_val = self.sha_hash(bytes(val, 'utf-8'))

        bit_string = ''
        for b in byte_val:
            if len(bit_string) == self.f:
                break
            for i in range(8):
                if (b >> i) & 1:
                    bit_string += '1'
                else:
                    bit_string += '0'
                if len(bit_string) == self.f:
                    break
        # We want to insert the finger print, not the value
        fingerprint = bit_string
        i1 = int.from_bytes(byte_val, "big")
        hash_f = int.from_bytes(self.sha_hash(
            bytes(fingerprint, 'utf-8')), "big")
        # xor because I no longer need to rely on the value string to calculate a second hash in collisions.
        # I can get an alternate by xoring i1 and hash of a finger print to get the 2nd index later on
        i2 = i1 ^ hash_f
        # returning the really big indicies and the fingerprint to insert
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


# Initialize the cuckoo filter,
# need to give it how many entries you want in a bucket and the desired false positive rate
x = CuckooFilter(10, 4, .99)

x.insert("AA")
x.insert("AC")
x.insert("AG")
x.insert("AT")
x.insert("CA")
x.insert("CC")
x.insert("CG")
x.insert("CT")

# # lookup those keys probably exist
print('lookup presence for those in')
print(x.lookup("AA"))
print(x.lookup("AC"))
print(x.lookup("AG"))
print(x.lookup("AT"))
print(x.lookup("CA"))
print(x.lookup("CC"))
print(x.lookup("CG"))
print(x.lookup("CT"))

# # lookup for keys that likely do not exist
print('lookup presence for those not in')
print(x.lookup("GA"))
print(x.lookup("GC"))
print(x.lookup("GG"))
print(x.lookup("TT"))
print(x.lookup("TA"))
print(x.lookup("TC"))
print(x.lookup("TG"))
print(x.lookup("TT"))
