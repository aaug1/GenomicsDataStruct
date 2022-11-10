import hashlib, binascii
import numpy as np
import random

def is_prime(n):
  if n==2 or n==3: return True
  if n%2==0 or n < 2: return False
  for i in range(3, int(n**0.5)+1, 2):
    if n%i==0:
      return False
  return True

class BloomFilter:
  def __init__(self, num_hash=2, size=10):
    self.size = size
    all_hash = list(hashlib.algorithms_available)
    if len(all_hash) < num_hash:
      num_hash = len(all_hash)

    self.num_hash = num_hash

    self.hash_functions = []
    # for i in range(num_hash):
    #   next_hash = hashlib.new(all_hash[i])
    #   self.hash_functions.append(next_hash)
    self.bloom_filter = np.zeros(size)
    self.generateHashFunctions()
  
  def __str__(self):
    return f"Bloom Filter: {self.bloom_filter}"

  def generateHashFunctions(self):
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
       
  def hashStr(self, str_to_hash, hash_fun):
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
    for i in range(self.num_hash):
      hash = self.hash_functions[i]
      index = self.hashStr(key, hash)
      self.bloom_filter[index] = 1

  def check(self, key):
    for i in range(self.num_hash):
      hash = self.hash_functions[i]
      index = self.hashStr(key, hash)
      if self.bloom_filter[index] == 0:
        print(f"Key: {key} does not exist in the database")
        return 0
    
    print(f"Key {key} probably exists in the database")
    return 1


# Initialize the bloom filter
x = BloomFilter()

# Store sequence of keys
x.store("a")
x.store("b")
x.store("c")

print(x)
# Check those keys probably exist
x.check("a")
x.check("b")
x.check("c")

# Check for keys that likely do not exist
x.check("d")
x.check("e")
x.check("f")