import hashlib
import numpy as np
import random


def is_prime(n):
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n < 2:
        return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0:
            return False
    return True


class BloomFilter:
    def __init__(self, num_hash=2, size=10):
        """Generates bloom filter with universal hash family"""
        self.size = size
        all_hash = list(hashlib.algorithms_available)
        if len(all_hash) < num_hash:
            num_hash = len(all_hash)
        self.num_hash = num_hash
        self.hash_functions = []
        self.bloom_filter = np.zeros(size)
        self.true_data = set()
        self.generateUniHashFunctions()

    def __str__(self):
        return f"Bloom Filter: {self.bloom_filter}"

    def generateUniHashFunctions(self):
        """Generates universal hash family using primes"""
        primes = []
        poss_prime = 2

        while len(primes) < self.num_hash:
            if is_prime(poss_prime):
                primes.append(poss_prime)
            poss_prime += random.randint(1, 10000)

        for i in range(self.num_hash):
            a = random.randint(1, primes[i])
            b = random.randint(0, primes[i])
            c = random.randint(1, primes[i])
            self.hash_functions.append((a, b, c, primes[i]))

    def setHashFunctions(self, hash_functions):
        """Sets custom hash functiosn following form (a, b, c, d)"""
        self.hash_functions = []
        self.bloom_filter = np.zeros(self.size)
        for quad in hash_functions:
            self.hash_functions.append(quad)

    def hashStr(self, str_to_hash, hash_fun):
        """Returns the hashed index value for a string"""
        if not isinstance(str_to_hash, str):
            str_to_hash = str(str_to_hash)

        a, b, c, p = hash_fun
        str_to_hash = "1" + str_to_hash
        l = len(str_to_hash) - 1

        int_to_hash = 0
        for i in range(l+1):
            int_to_hash += ord(str_to_hash[i]) * (c ** (l-i))
        int_to_hash = int_to_hash % p
        return ((a * int_to_hash + b) % p) % self.size

    def store(self, key):
        """Stores a key in bloom filter"""
        for i in range(self.num_hash):
            hash = self.hash_functions[i]
            index = self.hashStr(key, hash)
            self.bloom_filter[index] = 1
        self.true_data.add(key)
      
    def store_return_indices(self, key):
        indices = []
        for i in range(self.num_hash):
            hash = self.hash_functions[i]
            index = self.hashStr(key, hash)
            self.bloom_filter[index] = 1
            indices.append(index)
        self.true_data.add(key)
        return indices

    def check(self, key):
        """Determines if key is probably in bloom filter or not"""
        for i in range(self.num_hash):
            hash = self.hash_functions[i]
            index = self.hashStr(key, hash)
            if self.bloom_filter[index] == 0:
                print(f"Key: {key} does not exist in the database")
                return 0

        print(f"Key {key} probably exists in the database")
        return 1
      
    def check_return_indices(self, key):
        """Determines if key is probably in bloom filter or not, returning mapped indices"""
        indices = []
        for i in range(self.num_hash):
            hash = self.hash_functions[i]
            index = self.hashStr(key, hash)
            indices.append(index)

        return indices

    def is_false_positive(self, key):
        """checks if a key is a false positive or not"""
        for i in range(self.num_hash):
            hash = self.hash_functions[i]
            index = self.hashStr(key, hash)
            if self.bloom_filter[index] == 0:
                print(f"Key: {key} does not exist in the database")
                return 0

        print(f"Key {key} probably exists in the database. Checking...")
        if key in self.true_data:
            print(f"Key {key} was found. True positive.")
            return 0
        else:
            print(f"Key {key} was not found in true data. False positive.")
            return 1


