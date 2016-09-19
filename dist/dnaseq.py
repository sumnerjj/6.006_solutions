#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *
from sets import Set

### Utility classes ###

# Maps integer keys to a set of arbitrary values.
class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        self.dic = dict()
        for pair in pairs:
            key = pair[0]
            values = pair[1]
            if not self.dic.get(key):
                self.dic[key] = Set()
            for value in values:
                self.dic[key].add(value)

    # Associates the value v with the key k.
    def put(self, k, v):
        if not self.dic.get(k):
            self.dic[k] = Set()
        self.dic[k].add(v)

    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        if not self.dic.get(k):
            return []
        else:
            return [ x for x in self.dic[k] ]



# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):
    index = 0
    sub = ''
    for i in seq:
        sub+=i
        if len(sub)>k:
            sub=sub[1:]
        if len(sub)==k:
            h =RollingHash(sub)
            yield (sub, h, index - k + 1)
        index += 1


# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    seq = iter(seq)
    index = 0
    sub = ''
    for i in seq:
        sub += i
        if len(sub) > k:
            sub = sub[1:]
        if len(sub) == k and (index + 1)%m == 0:
            h =RollingHash(sub)
            yield (sub, h, index - k + 1)
        index += 1

# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
    b_dict = Multidict()
    res = []

    for h in subsequenceHashes(b, k):
        b_dict.put( h[0], h[2] )

    for h in intervalSubsequenceHashes(a, k, m):
        values = b_dict.get(h[0])
        for v in values:
            res.append( (h[2], v) )
    return res

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0])
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
