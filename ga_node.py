# Nodes of the GA Tree
"""
Created on Thu Apr 12 11:44:04 2018

@author: vlado.filipovic
"""

import random

from anytree import NodeMixin, RenderTree, PostOrderIter

from bitstring import BitArray

# helper function that count elements in collection
def count(collection):
    i=0
    for node in collection:
        i+=1
    return i

# helper function that fids a postion of the element in collection
def indexOf(collection, element, start=0):
    for i in range(start, collection.length):
        if( i < start ):
            continue;
        if( collection[i]==element):
            return i;
    return -1

class GaNodeInfo(object):
    typeDescription = "GaNodeInfo"

class GaNode(GaNodeInfo, NodeMixin):  # Add Node feature
    
    def __init__(self, nodeLabel, binaryTag, parent=None):
        super(GaNodeInfo, self).__init__()
        self.nodeLabel = nodeLabel
        self.binaryTag = binaryTag
        self.parent = parent

    # function for printing GA subtree
    def printGaSubtree( self, endS = '\n'):
        for pre, _, node in RenderTree(self):
            treestr = u"%s%s" % (pre, node.nodeLabel)
            print(treestr.ljust(8), node.binaryTag.bin )
        print(end=endS)
        return
    
    # function for adding child GA node
    def attachAsChild( self, child):
        child.parent = self
        return

    def flipNodeLabel(self):
        self.nodeLabel = self.nodeLabel.strip()
        if(self.nodeLabel.endswith('+')):
            self.nodeLabel = self.nodeLabel[:-1] + '-'
        elif(self.nodeLabel.endswith('-')): 
            self.nodeLabel = self.nodeLabel[:-1] + '+'
        return

    # initialization od the tree
    def initializeTree(self, labels, size):
        currentTreeSize = 1
        probabilityOfNodeCreation = 0.9
        for i in range(2 * size):
               if( random.random() < probabilityOfNodeCreation):
                   # create new leaf node
                   labelToInsert = random.choice( labels ) + '+'
                   leafBitArray = BitArray()
                   leaf = GaNode(labelToInsert, leafBitArray)
                   # find the parent of the leaf node
                   position = random.randint(0, currentTreeSize)
                   if( position == 0):
                       parentOfLeaf = self
                   else:
                       j = 1
                       for node in PostOrderIter(self):
                           if( j== position):
                               parentOfLeaf = node
                               break
                           else:
                               j += 1    
                   # attach leaf node
                   parentOfLeaf.attachAsChild(leaf)
                   leaf.binaryTag.append( leaf.parent.binaryTag )
                   # set binary tag
                   indexBit = count( leaf.parent.children )-1
                   indexBit = indexOf( leaf.binaryTag, False, start = indexBit)
                   if( indexBit >= 0):
                       leaf.binaryTag.invert(indexBit)
                   # reverse reverse label, if necessary
                   node = leaf.parent
                   while( node.parent != None):
                       if( leaf.nodeLabel == node.nodeLabel):
                           leaf.flipNodeLabel()
                           break
                       if( leaf.nodeLabel[:-1] == node.nodeLabel[:-1]):
                           break
                       node = node.parent
                   currentTreeSize += 1 
                   # delete leaf is label is duplicate
                   for node in leaf.parent.children:
                       if( node.nodeLabel == leaf.nodeLabel and node != leaf):
                           leaf.parent = None;
                           currentTreeSize -= 1
                           break
               if( i > size ):
                    probabilityOfNodeCreation *= 0.6
        return
        
     # compression od the tree
    def compressTree(self):
        for n in self.children:
            for c in n.children:
                if( n.nodeLabel[:-1] == c.nodeLabel[:-1]):
                    for x in c.children:
                        x.parent = self
        #for n1 in self.children:
        #    for n2 in self.children:
        #        if n1.nodeLabel == n2.nodeLabel and n1!=n2:
        #            n2.parent = None
        #            for c in n2.children:
        #                c.parent = n1  
        for n in self.children:
             n.compressTree()
        return
         
# initialization of the individual
def initIndividual(ind_class, labels, size):
    rootBitArray = BitArray(int = 0, length = size)
    root = ind_class('--', rootBitArray)
    root.initializeTree( labels, size)
    #root.compressTree()
    return root

# mutation
def mutation(individual):
    individual.printTree()
    #randomIndex = random.choice(individual.children)
    return (individual,)

# evaluation
def evaluation(individual):
    return (individual),
  