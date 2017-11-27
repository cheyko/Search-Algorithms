#!/bin/python

## Compute the mode of a given set of numbers read in from stdin

import sys
import time
import collections

def findMode(arr):
    
    maxFreq = 0
    modalVal = None
    uniques = 0
    freq = collections.defaultdict(int)
    for v in arr:
        count = freq[v] + 1
        freq[v] = count
        if count == 1:
            uniques += 1
        if count > maxFreq:
            maxFreq = count
            modalVal = v
    return (modalVal, maxFreq, uniques)

def readValues(n):
    """Return an iterator for n values read from stdin"""
    for i in xrange(n):
        yield int(raw_input().strip())

def main():
    n = int(raw_input().strip())
    (mode, freq, uniques) = findMode(readValues(n))
    print("%d %d %d" % (mode, freq, uniques))

if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()
    print ("Time taken = %f" % (t1 - t0))

