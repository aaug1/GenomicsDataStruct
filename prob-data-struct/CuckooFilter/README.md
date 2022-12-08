# Cuckoo Filter

<img src="https://i.ibb.co/34WQTrB/cuckoo-filter.png" alt="drawing" width="500"/>

## Motivation

So we just saw how bloom filters worked, so what are cuckoo filters, and how does it improve upon a bloom filter?

Similar to bloom filters, **cuckoo filters** are a _probabilistic data structure_ that, in response to a search or query of a key, will return either

Just like hash tables, this occurs in approximately/amortized O(1) lookup time. Sometimes we need to delete an item from our data structure. Bloom filters
risk removing multiple items if some of the indices revert back to 0 because some indices being 1 can have overlap with multiple items. With Cuckoo Filters, the fingerprint help with avoiding overlap, but the user
must still know that an item existed before deciding to delete.

## What does this have to do with cuckoo?

The cuckoo, which is a bird, is a savage. It's a brood parasite because they lay their eggs in another bird's
nest. When the cuckoo hatches, they also push off any other eggs in the next. This is related to how
a cuckoo filter will kick out an item to another index when there is no more space to be inserted.

## Applications

_Genomics_

-Removing duplicates of Reads

_Other applications_

- Database query time saving.

## Pros

1. Supports deletion
2. No false negatives! You can be sure of a "no" if it returns "no"
3. There is a capped false positive rate
4. Actual elements are not stored (ensures privacy of data)
5. Can modify settings to suit your needs!

## Cons

1. Can fail to add an element
2. Uncertainty in true positives

For an in-depth guide into cuckoo filters with explanation, please click the following link:

https://www.youtube.com/watch?v=R53DZvx8paE&ab_channel=MarkTiavises
