#!/bin/python

import time
import bst


#****************************************************************FindMode using BINARY SEARCH TREE implementation******************************************************************************


def findMode(arr):
    """ find the modal max frequency and unique values in an array of n values"""
    
    #*********************************************************************
    #@param : an array of n elements in read from prompt                 *
    #@return : the value that appears the most in the tree, it frequency *
    #          and also the number of unique numbers                     *
    #*********************************************************************
    
    tree = bst.BST()
    modalVal = 0
    maxFreq = 0
    uniques = 0
    for k  in arr:
        node = tree.search(k)
        if node == None:
            tree.insert(k,1)
            uniques+=1
        else:
            if node.key == k:
                node.value+=1
                if node.value > maxFreq:
                    maxFreq = node.value
                    modalVal = k
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
## Signed for ID# 620077109 at 2017-04-03 22:34:23.298725
## 789495a21eccdb25adad2c3328f45614b32d6aab
