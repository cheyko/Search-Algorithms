#!/bin/python

import sys
import time
import os
import re
import silly_list_mode,fast_list_mode
import rbtree_mode, dict_mode, bst_mode

# tests = ['tiny', 'small', 'medium', 'large',
#          'xlarge', 'xlarge02', 'xlarge03', 'xlarge04',
#          'xxlarge']

testCasePat = re.compile(r'(.*)-input\.txt')

def getInputFiles(folder):
    filenames = map(lambda f: os.path.join(folder, f), os.listdir(folder))
    filenames.sort()
    return filenames

def getTestStems(filenames):
    stems = []
    for name in filenames:
        m = testCasePat.match(name)
        if m != None:
            stems.append(m.group(1))
    return stems

algorithms = [dict_mode.findMode, silly_list_mode.findMode,
              fast_list_mode.findMode, bst_mode.findMode, rbtree_mode.findMode]

def mkFormatStr(n):
    """Return a format string suitable for formatting titles"""
    return ", %s" * n

def getTitles(algList):
    modulePat = re.compile(r'(\w+)_mode')
    def extractModuleTitle(fn):
        moduleName = fn.__module__
        m = modulePat.search(moduleName)
        if m != None:
            return m.group(1)
        else:
            return "<unknown>"
    return map(extractModuleTitle, algList)

def main(tests, algorithms):
    # print ("%s, %s,, %s,, %s,, %s,, %s,, %s,, %s" % \
    #        ('Test', 'Size', 'dict', 'silly_list', 'slow_list', 'slow2_list', 
    #         'fast_list', 'rbtree'))
    # Accommodate Test, Size and #uniques fields
    fmt = "%s, %s, %s" + mkFormatStr(len(algorithms))
    titles = ["Test", "Size", "#Uniques"] + getTitles(algorithms)
    print(fmt % tuple(titles))
    results = []
    for test in tests:
        inputFile = test + '-input.txt'
        answerFile = test + '-output.txt'
        inpLst = []
        with open(inputFile, 'r') as infile:
            n = int(infile.readline().strip())
            for i in xrange(n):
                inpLst.append(int(infile.readline().strip()))
            uCount = len(set(inpLst))

        with open(answerFile, 'r') as ansfile:
            (mVal, mFreq) = map(int, ansfile.readline().strip().split(' '))

        # print the test name, the input size, and the unique count
        print("%s, %d, %d" % (os.path.basename(test), n, uCount)),
        timings = [inputFile]
        for findMode in algorithms:
            stime = time.time()
            (mode, freq, uniques) = findMode(inpLst)
            ftime = time.time()
            correct = (mVal == mode) and (mFreq == freq)
            dur = (ftime - stime)
            print(", %f" % (dur if correct else -1.0)),
            timings.append((correct, dur))
        print
        results.append(timings)

def usage():
    print("%s <testdir>" % sys.argv[0])
    print("Print to stdout a series of timing tests indicating the time taken")
    print("by each algorithm on the test data provided in the test directory")
    print("Currently, timing data will be printed for the following algorithms")
    print("silly_list, slow_list, slow2_list, fast_list, dict, rbtree")

if __name__ == "__main__":
    if len(sys.argv) < 1:
        usage()
        exit
    else:
        testDir = sys.argv[1]
        if os.path.isdir(testDir):
            tests = getTestStems(getInputFiles(testDir))
        else:
            tests = getTestStems(sys.argv[1:])
        main(tests, algorithms)
