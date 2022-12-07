# Bloom Filter

<img src="https://i.ibb.co/54p7fBR/bloom-filter.png" alt="drawing" width="500"/> 

## Motivation

Hash tables are frequently implemented for data storage due to the
fast lookup time of a query / search. However, what if we had more rigorous
size constraints? Or

**Bloom Filters** are a *probabilistic data structure* that, in response to a search or query of a key, will return either

1. **Probably** yes  
2. Definitely no

As a result, Bloom Filters can 100% accurately report if an element does not in a database (false negatives are not possible), but cannot guarantee if an item exists in the data base (false positives are possible).

Just like hash tables, this occurs in approximately/amortized O(1) lookup time. However, the size of this data structure can be much smaller in exchange for its uncertain predictions!

## What does this have to do with flowers?

The "Bloom" part of the Bloom Filter refers to how keys are hashed to indices in the data strcture. Specifically, each key is passed through multiple hash functions, which map it to various outputs. This creates a "bloom" type of mapping!

When searching for a key, we input it into all of the hash functions and check all related indices. If all mapped values are 1's, then the key probably exists in the data structure. However, if a single index is a 0, we know that the key does not exist (or else it would have mapped to one of the keys!)

## Applications
*Genomics*
* Testing existence of k-mer in a sequence

*Other applications*
* Prevent weak passwords
* Caching
* Database queries

## Pros
1. Uses constant space
2. No false negatives! You can be sure of a "no" if it returns "no"
3. Can never fail to add an element
4. Actual elements are not stored (ensures privacy of data)
5. Can modify settings to suit your needs!

## Cons
1. Cannot remove items from bloom filters.
2. Uncertainty in true positives
