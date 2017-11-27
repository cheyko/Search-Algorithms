#!/bin/python

## Binary Tree ADT

class Node:
    def __init__(self, key, value=None):
        self._key = key
        self._value = value

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

class BST:
    def __init__(self, root=None):
        """Make an empty tree if root is None"""
        if root == None:
            self.root = None
            self.left = None
            self.right = None
        else:
            self.root = root
            self.left = BST()
            self.right = BST()

    def isEmpty(self):
        return self.root == None

    def mkLeaf(self, node):
        self.root = node
        self.left = BST()
        self.right = BST()

    def isLeaf(self):
        return self.left.isEmpty() and self.right.isEmpty()

    def insert(self, key, value=None):
        """Associate the key with the given value in this BST.  Return the
        node containing the given key."""

        #********************************************************************
        #@param: the key and value your assigning to the node your creating *
        #return : a node instance that was created and stored in memory     *
        #********************************************************************

        treeRoot = self.root
        treeL = self.left
        treeR = self.right
        if self.isEmpty():                  # if is empty then the value of the root is None then it means that the tree is empty and if it empty(view next line)
            treeRoot =  Node(key,value)     # we make the inserted value the root.
            self.mkLeaf(treeRoot)           # after the insert node become the root make leaf is called on it to make the left and right of the tree subtrees and the root a node.
            return treeRoot                 # returns the node.
        elif treeRoot.key > key:
            return treeL.insert(key,value)  # if the key with value you want to insert is less that the key of the root, insert it in the left subtree.
        else:
            return treeR.insert(key,value)  # if the key with value you want to insert is greater that the key of the root, insert it in the right subtree.

    def search(self, key):
        """Return the node containing the given key, or None if the key is not
        found."""

        #*******************************************************************************
        #@param : the key that your seaching for in the binary search tree             *
        #@return : the node instance that is associated with the key you use to search *
        #*******************************************************************************

        treeRoot = self.root
        treeL = self.left
        treeR = self.right
        if not self.isEmpty():
            if treeRoot.key == key:       # if the key you enter is equal to a key found in the tree.
                return treeRoot           # return the value for that key.
            elif treeRoot.key > key:      # if the key your seaching for is less than the key of the root it means that the key your looking for is in the left subtree.
                return treeL.search(key)  # call back search to search the left substree with the key.
            else:
                return treeR.search(key)  # call back search to search the right substree with the key.
        return None


## --
## Do not edit below this line
## Signed for ID# 620077109 at 2017-04-03 22:34:23.296037
## 47e5ad8285df84ce361e05a1c245b0c644e6803a
