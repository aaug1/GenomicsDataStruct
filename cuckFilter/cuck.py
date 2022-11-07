import hashlib
import math

#https://www.pdl.cmu.edu/PDL-FTP/FS/cuckoo-conext2014.pdf
#https://medium.com/@meeusdylan/implementing-a-cuckoo-filter-in-go-147a5f1f7a9
class CuckooFilter:
  # n = len(items), fp = false positive rate
    def __init__(self, n: int, fp: float):
        self.b = 4  # entries per bucket
        self.f = self.fingerprintLength(self.b, fp) #How long a fingerprint in bytes
        numBits = int((n / self.f) * 8)
        self.m = self.nextPower(numBits)  # buckets
        self.buckets = [[None]*self.m for i in range(self.b)]
        self.n = n  # filter capacity (rename cap?)
        
    def insert(self, input: str):
        i1, i2, f = self.hashes(input)
        # The modulo self.m is to cap the hash so it can be used as an actual index
        if self.buckets[i1 % self.m] is None:
            self.buckets[i1 % self.m] = f
            return
        if self.buckets[i2 % self.m] is None:
            self.buckets[i2 % self.m] = f
            return
        
        '''I need to kick stuff out and check cycles if too many'''

    def hashes(self, val: str):
        h = self.sha_hash(bytes(val, 'utf-8'))
        fingerprint = h[0: self.f] #We want to store the finger print, not the value
        i1 = int.from_bytes(h, "big")
        hash_f = int.from_bytes(self.sha_hash(fingerprint), "big")
        #xor because I no longer need to rely on the value string to calculate a second hash in collisions.
        #I can get an alternate by xoring i1 and hash of a finger print to get the 2nd index later on
        i2 = i1 ^ hash_f
        #returning the really big indicies and the fingerprint to store
        #the modulo self.m is to cap the i1 nad i2 to be indicies of the actual buckets array
        return i1, i2, fingerprint

    #val must already be in bytes
    def sha_hash(self, byte_val):
        hashObj = hashlib.sha1(byte_val)
        return hashObj.digest()
    
    #returns the length of finger print in bytes
    def fingerprintLength(self, b: int, e: float):
        f = math.ceil(math.log(2 * float(b) / e))
        f /= 8 #divide by 8 to get the number of bytes
        if f < 1:
            return 1
        return f  # We want to limit the bytes to at least 1.
    
    #https://cs.stackexchange.com/questions/81876/cuckoo-filters-for-non-powers-of-2
    #So apparently the storage in cuckoo should be a power of 2 if you want 95% load factor 
    #Mark I need to look at this again
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

p1.insert('somethiqweng')

#print(len(p1.buckets[0]))
