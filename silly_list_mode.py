#!/bin/python

## Compute the mode of a given set of numbers read in from stdin

import sys
import time

def insert(lst, v):
    n = len(lst)
    i = 0
    while i < n:
        (vv, freq) = lst[i]
        #print(lst[i])
        if vv == v:
            count = freq + 1
            lst[i] = (v, count)
            #print(count)
            return count
        else:
            i = i + 1
    lst.append((v, 1))
    return 1

def findMode(arr):
    maxFreq = 0
    modalVal = None
    seen = []
    nUnique = 0
    for v in arr:
        count = insert(seen, v)
        if count > maxFreq:
            maxFreq = count
            modalVal = v
        if count == 1:
            nUnique += 1
    return (modalVal, maxFreq, nUnique)

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

