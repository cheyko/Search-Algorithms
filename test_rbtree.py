#!/bin/python

import unittest
import rbtree

class TestRBTree(unittest.TestCase):
    def setUp(self):
        self.rbt = rbtree.RBTree()

    def tearDown(self):
        self.rbt.show()
        self.rbt = None

    def test_insert(self):
        print('Insert')
        self.rbt.insert(50)
        self.rbt.insert(20)
        self.rbt.insert(70)
        r = self.rbt.root
        self.assertEqual(r.key, 50)
        self.assertEqual(r.left.key, 20)
        self.assertEqual(r.right.key, 70)
        self.rbt.insert(100)
        self.assertEqual(r.right.right.key, 100)

    def test_4nodeCC(self):
        print('4 Node CC')
        self.rbt.insert(50)
        self.rbt.insert(20)
        self.rbt.insert(70)
        self.rbt.insert(100)
        rt = self.rbt.root
        rr = rt.right.right
        self.assertEqual(rr.key, 100)
        self.assertEqual(rr.colour, rbtree.RED)
        self.assertEqual(rt.left.colour, rbtree.BLACK)
        self.assertEqual(rt.right.colour, rbtree.BLACK)
        self.assertEqual(rt.colour, rbtree.BLACK)

    def test_3nodeCC(self):
        print('3 Node CC')
        tests = [(0, 1, 2), (0, 2, 1), (2, 1, 0), (2, 0, 1)]
        values = [50, 70, 100]
        for (i, j, k) in tests:
            rbt = rbtree.RBTree()
            rbt.insert(values[i])
            rbt.insert(values[j])
            rbt.insert(values[k])
            rt = rbt.root
            self.assertEqual(rt.colour, rbtree.BLACK)
            self.assertEqual(rt.key, values[1])
            self.assertEqual(rt.left.colour, rbtree.RED)
            self.assertEqual(rt.right.colour, rbtree.RED)
            self.assertEqual(rt.left.key, values[0])
            self.assertEqual(rt.right.key, values[2])
            print("Test %s passed!" % str((i, j, k)))

    def test_ascending_inserts(self):
        print('Ascending Inserts')
        BLACK = rbtree.BLACK
        RED = rbtree.RED
        for k in [10, 20, 30, 40, 50, 60, 70, 80]:
            self.rbt.insert(k)
        r = self.rbt.root
        self.assertEqual(r.key, 40)
        self.assertEqual(r.colour, BLACK)
        self.assertEqual(r.left.key, 20)
        self.assertEqual(r.left.colour, RED)
        self.assertEqual(r.left.left.key, 10)
        self.assertEqual(r.left.left.colour, BLACK)
        self.assertEqual(r.left.right.key, 30)
        self.assertEqual(r.left.right.colour, BLACK)
        self.assertEqual(r.right.key, 60)
        self.assertEqual(r.right.colour, RED)
        self.assertEqual(r.right.left.key, 50)
        self.assertEqual(r.right.left.colour, BLACK)
        self.assertEqual(r.right.right.key, 70)
        self.assertEqual(r.right.right.colour, BLACK)
        self.assertEqual(r.right.right.right.key, 80)
        self.assertEqual(r.right.right.right.colour, RED)
        
    def test_successor(self):
        print('Successor')
        keys = [10, 20, 30, 40, 50, 60, 70, 80]
        for k in keys:
            self.rbt.insert(k)
        out = []
        (isFound, node) = self.rbt.search(10)
        print(node.key)
        self.assertTrue(isFound)
        while node != None:
            out.append(node.key)
            node = self.rbt.successor(node)
        self.assertEqual(out, keys)


    def test_predecessor(self):
        print('Predecessor')
        keys = [10, 20, 30, 40, 50, 60, 70, 80]
        for k in keys:
            self.rbt.insert(k)
        out = []
        (isFound, node) = self.rbt.search(80)
        self.assertTrue(isFound)
        while node != None:
            out.append(node.key)
            node = self.rbt.predecessor(node)
        keys.reverse()
        self.assertEqual(out, keys)
        
        

if __name__ == '__main__':
    unittest.main()

