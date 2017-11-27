#!/bin/python

## Compute the mode of a given set of numbers read in from stdin

import sys
import time
from sortedcontainers import SortedList

#****************************************************************FindMode using sorted list and binary implementation******************************************************************************
        
    
    #*******************************************************************************
    #@param : a list, a value to search for and a boolean flag                     *
    #@return : binary search function searches a list determine whether a value is *
    #          in the list are not                                                 *
    #*******************************************************************************
    
    
def Insert_binarySearch(lst,k):
    high = len(lst)-1
    low = 0
    while low<=high:
        mid = low + (high-low)//2 
        (cc,freq) = lst[mid]       
        if cc == k:                
            count = freq + 1
            lst[mid] = (k,count)
            return count
        elif k < cc:
            high = mid - 1
        else:
            low = mid + 1
    lst.add((k,1))
    return 1
        
        
def findMode(arr):
    
    #****************************************************************************
    # Implement this to use a Python list along with binary search to maintain  *
    # and search the set of elements previously seen                            *
    #****************************************************************************
    #@return : return the value that appears the most in the tree, it frequency *
    #          and also the number of unique numbers                            *
    #****************************************************************************

    modalVal = None
    maxFreq = 0
    uniques = 0
    lst = SortedList()
    for k  in arr:
       count = Insert_binarySearch(lst,k)
       if count > maxFreq:
           maxFreq = count
           modalVal = k
       if count == 1:
           uniques += 1
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


## --
## Do not edit below this line
## Signed for ID# 620077109 at 2017-04-03 22:34:23.300755
## 2a7e9e8bdca2a4d86824a8c8760dea34234e9ccb
