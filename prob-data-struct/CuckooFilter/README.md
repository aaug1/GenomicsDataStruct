# Cuckoo Filter

<img src="https://i.ibb.co/34WQTrB/cuckoo-filter.png" alt="drawing" width="500"/> 

## Motivation

So we just saw how bloom filters worked, so what are cuckoo filters, and how does it improve upon a bloom filter?

Similar to bloom filters, **cuckoo filters** are a *probabilistic data structure* that, in response to a search or query of a key, will return either


Just like hash tables, this occurs in approximately/amortized O(1) lookup time. Sometimes we need to delete an item from our data structure. Bloom filters
risk removing multiple items 

## What does this have to do with cuckoo?


## Applications
*Genomics*
* 

*Other applications*
* 
* 
* 

## Pros
1. Uses constant space
2. No false negatives! You can be sure of a "no" if it returns "no"
3. Can never fail to add an element
4. Actual elements are not stored (ensures privacy of data)
5. Can modify settings to suit your needs!

## Cons
1. Cannot remove items from bloom filters.
2. Uncertainty in true positives

For an in-depth guide into cuckoo filters with explanation, please click the following link:

https://www.youtube.com/watch?v=R53DZvx8paE&ab_channel=MarkTiavises