#!/bin/python

### Module that implements a Red-Black Tree

BLACK = 1
RED = 0

class RBTree:

    class Node:
        """Nodes specific to this RBTree.  Nodes point at trees and trees
        point at nodes.  This will allow rotations that change the
        root.

        """
        def __init__(self, parent, key, value, colour=RED, sentinel=None):
            self._parent = parent
            self._key = key
            self._value = value
            self._colour = colour
            self._left = sentinel
            self._right = sentinel

        parent = property(fget=lambda self: self._parent,
                          doc="The node's parent")
        @parent.setter
        def set_parent(self, p):
            self._parent = p

        key = property(fget = lambda self: self._key,
                       doc="The node's key")
        @key.setter
        def set_key(self, k):
            self._key = k

        @property
        def value(self):
            """The value associated with this node's key"""
            return self._value

        @value.setter
        def set_value(self, v):
            self._value = v
        
        colour = property(fget=lambda self: self._colour,
                          doc="The node's colour, RED = 0, BLACK = 1")

        @colour.setter
        def set_colour(self, c):
            self._colour = c
        
        left = property(fget=lambda self: self._left,
                        doc="The node's left child")
        @left.setter
        def set_left(self, l):
            self._left = l


        right = property(fget=lambda self: self._right,
                         doc="The node's right child")

        @right.setter
        def set_right(self, r):
            self._right = r
            

        def __str__(self):
            return ("<value: %s, colour: %s,%n  parent: %s,%n  left: %s,%n  right: %s%n>" %
                    (self.key, self.colour, 
                     self.parent, self.left, self.right))

    ## --- Start of RB-Tree methods ---

    def __init__(self):
        self._NIL = list()
        self._root = self._NIL

    NIL = property(fget=lambda self: self._NIL, doc="Constant sentinel NIL")
    root = property(fget=lambda self: self._root, doc="The current root node")

    @root.setter
    def set_root(self, r):
        self._root = r

    def isRoot(self, node):
        return self.root == node
        
    def search(self, key):
        """Returns a tuple in the format (Found?, Node).  The first part of
        the tuple is True if the node was found and False
        otherwise. The node component of the result is the node
        containing key if it was already present, otherwise returns the
        node that would be the parent of where key would have been
        found in the tree.  (This latter choice of returned node
        avoids having to search the tree twice when inserting a new
        key into the tree)

        """
        ##**************************************************************
        ##@param key: is the key of the root where u start your search *
        ##@return parent or node                                       *
        ##**************************************************************
        
        parent = self.NIL
        curr = self.root
        while curr != self.NIL:
            if key == curr.key:
                return (True, curr)
            elif key < curr.key:
                parent = curr
                curr = curr.left  
            else:
                parent = curr
                curr = curr.right
        return (False, parent)

    def contains(self, key):
        (foundP, where) = self.search(key)
        return foundP

    def lookup(self, key, defaultVal=None):
        (foundP, where) = self.search(key)
        if foundP:
            return where.value
        else:
            return defaultValue

    def getNode(self, key, defaultVal):
        """Retrieve the value associated with key, but if key is not bound
        then associate it with defaultVal"""
        (foundP, where) = self.search(key)
        if foundP:
            return where
        else:
            return self._addChild(where, key, defaultVal)

    def insert(self, key, value=None):
        (wasFound, node) = self.search(key)
        if wasFound:
            node.value = value
        else:
            self._addChild(node, key, value)

    def _addChild(self, parent, key, value):
        child = self.Node(parent, key, value, RED, self.NIL)
        if parent == self.NIL: # at the root, special case
            self.root = child
        elif key < parent.key:
            parent.left = child
        else:
            parent.right = child
        self.validate(child)
        return child
            
    def insertMany(self, keys_values):
        for k,v in keys_values:
            self.insert(k, v)

    def validate(self, node):
        """Check that node's colour is correct for its position, and correct
        it if there is a violation of the RBTRee colour rules.

        """
        if node.colour == BLACK:
            return
        if self.isRoot(node):
            node.colour = BLACK
            return
        elif node.parent.colour == BLACK:
            return
        else:
            # We have a critical cluster here
            ccRoot = node.parent.parent
            self.fixCC(ccRoot)
            
    def swap_colour(self,node,nodeChild):
        
        ##*************************************************
        ## @param: the two nodes that is swapping colours *
        ##                                                *
        ##*************************************************
        
        nColour = node.colour                       # store the color of the parent node in the variable nColour
        ncColour = nodeChild.colour                 # store the color of the node child in the variable ncChild
        node.colour = ncColour                      # set the parent node colour to the colour of the node's child
        nodeChild.colour = nColour                  # set the node's child colour to the colour of the parent node

    def fixCC(self, ccroot):
        """Fixes a critical cluster rooted at ccroot.  Determines whether it
        is a 3- or 4-node critical cluster, and applies the appropriate
        correction to the cluster."""

        ##*************************************************
        ## Fix two of the 3-node CC cases                 *
        ## RIght Right case AND Right Left case           *
        ##*************************************************
        
        if ccroot.left == self.NIL or ccroot.left.colour == BLACK:
            if ccroot.right.right != self.NIL:         
                self.swap_colour(ccroot,ccroot.right)
                self.rotLeft(ccroot)                # do a left rotation at the root to fix right right case
            else:
                self.rotRight(ccroot.right)         # do a right rotation at the root's right child, which turn it in a right right case
                self.fixCC(ccroot)                  # so we do a resursive call on the root to fix right right case
                
        ##*************************************************
        ## Fix the other two 3-node cases here            *
        ## Left Left case AND Left Right case             *
        ##*************************************************
                
        elif ccroot.right == self.NIL or ccroot.right.colour == BLACK:
            if ccroot.left.left != self.NIL:
                self.swap_colour(ccroot,ccroot.left)
                self.rotRight(ccroot)               # do a right rotation at the root to fix left left case
            else:
                self.rotLeft(ccroot.left)           # do a left rotation at the root's left child, which turns the cluster it in a left left case
                self.fixCC(ccroot)                  # so we do a resursive call on the root to fix left left case
                
        ##*************************************************************
        ## We have a 4-node CC so recolour and check (validate) root. *
        ## Recolour                                                   *
        ##*************************************************************        
        else:
             ccroot.colour = RED                   # recolour the root to RED
             ccroot.left.colour = BLACK            # Recolour the root to BLACK
             ccroot.right.colour = BLACK           # Recolour the root to BLACK
             self.validate(ccroot)                 # Check that node's colour is correct for its position
               
#*************************************************************************************ROTATIONS****************************************************************************************************#             
                                                            ##************************************************************
                                                            ##                                                           *
                                                            ##            W                                 S            *
                                                            ##           / \                               / \           *
                                                            ##          /   \     Right-Rotate(S,W)       /   \          *
                                                            ##         S     Y        -------->          G     W         *
                                                            ##        / \             <--------               / \        *
                                                            ##       /   \        left-Rotate (W,S)          /   \       *
                                                            ##      G     U                                 U     Y      *
                                                            ##                                                           *
                                                            ##************************************************************
    def rotLeft(self, node):
        """Left rotate the sub-tree rooted at node.
        """
        p = node.parent
        rChild = node.right
        rlt = rChild.left
        rChild.left = node
        node.parent = rChild
        node.right = rlt
        if rlt != self.NIL:
            rlt.parent = node
        if p == self.NIL:
            self.root = rChild
        elif p.left == node:
            p.left = rChild
        else:
            p.right = rChild
        rChild.parent = p

    def rotRight(self, node):
        """Right-rotate the sub-tree rooted at node """
        p = node.parent
        lChild = node.left
        lrt = lChild.right
        lChild.right = node
        node.parent = lChild
        node.left = lrt
        if lrt != self.NIL:
            lrt.parent = node
        if p == self.NIL:
            self.root = lChild
        elif p.left == node:
            p.left = lChild
        else:
            p.right = lChild
        lChild.parent = p

    def show(self, node=None, indent=0):
        """Display the keys of the tree in a human readable manner""" 
        if node == None:
            node = self.root

        if node == self.NIL:
            print ('%s.' % (" " * (indent + 2)))
        else:
            if node.colour == BLACK:
                print('%s[%s]' % (" " * indent, node.key))
            else:
                print('%s(%s)' % (" " * indent, node.key))
            # Only show an empty if one branch is non-empty
            if node.left != self.NIL or node.right != self.NIL:
                self.show(node.left, indent + 2)
                self.show(node.right, indent + 2)

#***********************************************************Successor return the node that succedes a given node************************************************************************

    def minimum(self, node):
        """ Find the minimum value in a given tree"""
        
        #**************************************************************
        #@param: the root node of the tree your find the minimum of   *
        #@return: is the node with minimum key value in the tree      *
        #**************************************************************
        curr = node.right                 #set the node right child to a varaible
        updatedCurr = curr                #set the node right child to a varaible to keep track of update
        while curr != self.NIL:           
            updatedCurr = curr            # for each time the loop is ran the node in the varaible curr is assigned to updatedcurr varaible and
            curr = curr.left              # the varaible curr becomes the left child of the previous node that curr was assigned to and this constant occur until the loop is exited
        return updatedCurr                # the node with the minimum key is returned
        
    def successor(self,node):
        """ Displays the node that succedes a givn node"""
        
        #**************************************************************
        #@param node: is the node you want the successor for          *
        #@return:  the node that succedes the param node              *
        #**************************************************************
        
        if node.right != self.NIL:
            return self.minimum(node)
        nodePar = node.parent
        varNode = node
        while nodePar != self.NIL and varNode == nodePar.right:
                varNode = nodePar
                nodePar = varNode.parent
        if not nodePar != []:
            return None
        return nodePar

#******************************************************Predecessor return the node that succedes a given node****************************************************************************
    
    def maximum(self,node):
        """ Find the maximum value in a given tree"""
        
        #**************************************************************
        #@param: the root node of the tree your find the maximum of   *
        #@return: is the node with maximum key value in the tree      *
        #**************************************************************
        curr = node.left                    # set the node left child to a varaible
        updatedCurr = curr                  # set the node left child to a varaible to keep track of update
        while curr != self.NIL:
            updatedCurr = curr              # for each time the loop is ran the node in the varaible curr is assigned to updatedcurr varaible and
            curr = curr.right               # the varaible curr becomes the right child of the previous node that curr was assigned to and this constant occur until the loop is exited
        return updatedCurr                  # the node with the maximum key is returned
    
    def predecessor(self,node):
        """ Displays the node that precedes a givn node"""
        
        #**************************************************************
        #@param node: is the node you want the predecessor for        *
        #@return:  the node that precedes the param node              *
        #**************************************************************
        
        if node.left != self.NIL:
            return self.maximum(node)
        nodePar = node.parent
        varNode = node
        while nodePar != self.NIL and varNode == nodePar.left:
            varNode = nodePar
            nodePar = nodePar.parent
        if not nodePar != []:
            return None
        return nodePar


    
#****************************************************************************TEST CASES***************************************************************************************************


def testInsert():
    rbt = RBTree()
    rbt.insert(50)
    rbt.insert(20)
    rbt.insert(70)
    assert rbt.root.key == 50
    assert rbt.root.left.key == 20
    assert rbt.root.right.key == 70
    rbt.insert(100)
    assert rbt.root.right.right.key == 100
    rbt.show()
    return True

def test4NodeCC():
    rbt = RBTree()
    rbt.insert(50)
    rbt.insert(20)
    rbt.insert(70)
    rbt.insert(100)
    rt = rbt.root
    rr = rt.right.right
    assert rr.key == 100
    assert rr.colour == RED
    assert rt.left.colour == BLACK
    assert rt.right.colour == BLACK
    assert rt.colour == BLACK
    return True

def test3NodeCC():
    tests = [(0, 1, 2), (0, 2, 1), (2, 1, 0), (2, 0, 1)]
    values = [50, 70, 100]
    for (i, j, k) in tests:
        rbt = RBTree()
        rbt.insert(values[i])
        rbt.insert(values[j])
        rbt.insert(values[k])
        rt = rbt.root
        assert rt.colour == BLACK
        assert rt.key == values[1]
        assert rt.left.colour == RED
        assert rt.right.colour == RED
        assert rt.left.key == values[0]
        assert rt.right.key == values[2]
        print("Test %s passed!" % str((i, j, k)))

def testAscendingInsertion():
    rbt = RBTree()
    for k in [80, 20, 30, 40, 50, 60, 70, 10]:
        rbt.insert(k)
    rbt.show()
    r = rbt.root
    assert r.key == 40
    assert r.colour == BLACK
    assert r.left.key == 20
    assert r.left.colour == RED
    assert r.left.left.key == 10
    assert r.left.left.colour == BLACK
    assert r.left.right.key == 30
    assert r.left.right.colour == BLACK
    assert r.right.key == 60
    assert r.right.colour == RED
    assert r.right.left.key == 50
    assert r.right.left.colour == BLACK
    assert r.right.right.key == 70
    assert r.right.right.colour == BLACK
    assert r.right.right.right.key == 80
    assert r.right.right.right.colour == RED
    return True
   


## --
## Do not edit below this line
## Signed for ID# 620077109 at 2017-04-03 22:34:23.297115
## d08a5962b6ba7e806fd30d1fcbbd485f36c6a802
