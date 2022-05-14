# Implementation of B+-tree functionality.

from index import *
import math

# You should implement all of the static functions declared
# in the ImplementMe class and submit this (and only this!) file.
class ImplementMe:

    # Returns a B+-tree obtained by inserting a key into a pre-existing
    # B+-tree index if the key is not already there. If it already exists,
    # the return value is equivalent to the original, input tree.
    #
    # Complexity: Guaranteed to be asymptotically linear in the height of the tree
    # Because the tree is balanced, it is also asymptotically logarithmic in the
    # number of keys that already exist in the index.
    @staticmethod
    def InsertIntoIndex( index, key ):

        if index.nodes == []:
            index = Index([Node()]*1)
            index.nodes[0] = Node(KeySet((key,-1)), PointerSet((0,0,0)))
        else:
            currentNode = index.nodes[0]
            tempTree = []
            currentNodeIndex = 0
            while(not is_Leaf(currentNode)):
                for i, item in enumerate(currentNode.keys.keys):
                    if (key < item) or item == -1:
                        if i == 0:
                            currentNodeIndex = currentNode.pointers.pointers[0]
                            currentNode = index.nodes[currentNode.pointers.pointers[0]]
                            break
                        if i == 1:
                            currentNodeIndex = currentNode.pointers.pointers[1]
                            currentNode = index.nodes[currentNode.pointers.pointers[1]]
                            break
                    elif (i+1 == len(currentNode.keys.keys)):
                        currentNodeIndex = currentNode.pointers.pointers[2]
                        currentNode = index.nodes[currentNode.pointers.pointers[2]]
                        break

            if(not is_Full(currentNode)):
                temp = []
                for i in currentNode.keys.keys:
                    if i != -1:
                        temp.append(i)
                if key != temp[0]:
                    temp.append(key)
                    temp.sort()
                else:
                    temp.append(-1)
                index.nodes[currentNodeIndex] = Node(KeySet((temp[0],temp[1])),PointerSet((index.nodes[currentNodeIndex].pointers.pointers)))
            else:
                tempTable = list(currentNode.keys.keys)
                tempTable.append(key)
                tempTable.sort()
                splitIndex = math.ceil(len(tempTable)/2) - 1

                if(currentNodeIndex == 0):
                    tempTree = Index([Node()] * 4)
                    tempTree.nodes[0] = Node(KeySet((tempTable[splitIndex], -1)), PointerSet((1,2,0)))
                    tempTree.nodes[1] = Node(KeySet((tempTable[splitIndex-1], -1)), PointerSet((0,0,2)))
                    tempTree.nodes[2] = Node(KeySet((tempTable[splitIndex], tempTable[splitIndex+1])), PointerSet((0,0,0)))
                    return tempTree
                else:
                    parent = None
                    parentIndex = None
                    for i,item in enumerate(index.nodes):
                        if currentNodeIndex in item.pointers.pointers and item.pointers.pointers[0] != 0 and item.pointers.pointers[1] != 0:
                            parent = item
                            parentIndex = i

                    if(is_Full(parent)):
                        return index
                        
                    else:
                        parentKeys = list(parent.keys.keys)
                        parentKeys.append(tempTable[splitIndex])
                        parentKeys.remove(-1)
                        parentKeys.sort()

                        parentPointers = list(parent.pointers.pointers)

                        #newChild[list of keys, index, next_index]
                        newChild0 = [tempTable[:splitIndex],currentNodeIndex, currentNodeIndex+1]
                        newChild0[0].append(-1)

                        newChild1 = [tempTable[splitIndex:], currentNodeIndex + 1, None]

                        newChild2 = None
                        if newChild1[1] == parentPointers[1]:
                            newChild2 = [list(index.nodes[parentPointers[1]].keys.keys), parentPointers[1] + 1, 0]
                            newChild1[2] = newChild2[1]

                        if newChild2 == None:
                            newChild2 = [list(index.nodes[parentPointers[0]].keys.keys), parentPointers[0], min(newChild0[1],newChild1[1])]
                            newChild1[2] = 0

                        newChildren = [newChild0, newChild1, newChild2]
                        newChildren.sort(key = lambda newChildren: newChildren[1])

                        index.nodes[parentIndex] = Node( KeySet((parentKeys[0], parentKeys[1])), PointerSet((newChildren[0][1],newChildren[1][1],newChildren[2][1])))
                        index.nodes[newChildren[0][1]] = Node( KeySet((newChildren[0][0][0], newChildren[0][0][1])), PointerSet((0,0,newChildren[0][2])))
                        index.nodes[newChildren[1][1]] = Node( KeySet((newChildren[1][0][0], newChildren[1][0][1])), PointerSet((0,0,newChildren[1][2])))
                        index.nodes[newChildren[2][1]] = Node( KeySet((newChildren[2][0][0], newChildren[2][0][1])), PointerSet((0,0,newChildren[2][2])))

        return index

    # Returns a boolean that indicates whether a given key
    # is found among the leaves of a B+-tree index.
    #
    # Complexity: Guaranteed not to touch more nodes than the
    # height of the tree
    @staticmethod
    def LookupKeyInIndex( index, key ):
        if index.nodes == []:
            return False
        else:
            currentNode = index.nodes[0]
            while(not is_Leaf(currentNode)):
                for i, item in enumerate(currentNode.keys.keys):
                    if (key < item):
                        if i == 0:
                            currentNode = index.nodes[currentNode.pointers.pointers[0]]
                            break
                        if i == 1:
                            currentNode = index.nodes[currentNode.pointers.pointers[1]]
                            break
                    elif (i+1 == len(currentNode.keys.keys)):
                        currentNode = index.nodes[currentNode.pointers.pointers[2]]
                        break
            for item in currentNode.keys.keys:
                if item == key:
                    return True
        return False

    # Returns a list of keys in a B+-tree index within the half-open
    # interval [lower_bound, upper_bound)
    #
    # Complexity: Guaranteed not to touch more nodes than the height
    # of the tree and the number of leaves overlapping the interval.
    @staticmethod
    def RangeSearchInIndex( index, lower_bound, upper_bound ):
        myList = []
        if index.nodes == []:
            return []
        else:
            currentNode = index.nodes[0]
            while(not is_Leaf(currentNode)):
                for i, item in enumerate(currentNode.keys.keys):
                    if (lower_bound < item):
                        if i == 0:
                            currentNode = index.nodes[currentNode.pointers.pointers[0]]
                            break
                        if i == 1:
                            currentNode = index.nodes[currentNode.pointers.pointers[1]]
                            break
                    elif (i+1 == len(currentNode.keys.keys)):
                        currentNode = index.nodes[currentNode.pointers.pointers[2]]
                        break

            if (currentNode.pointers.pointers[2] == 0):
                for item in currentNode.keys.keys:
                    if item >= lower_bound and item < upper_bound:
                        myList.append(item)
            else:
                while(currentNode.pointers.pointers[2] != 0):
                    for item in currentNode.keys.keys:
                        if item >= lower_bound and item < upper_bound:
                            myList.append(item)
                    currentNode = index.nodes[currentNode.pointers.pointers[2]]
                for item in currentNode.keys.keys:
                    if item >= lower_bound and item < upper_bound:
                        myList.append(item)
        return myList

def is_Full(node):
    for i in node.keys.keys:
        if i == -1:
            return False
    return True

def is_Leaf(node):
    if node.pointers.pointers[0] == 0 and node.pointers.pointers[1] == 0:
        return True
    else:
        return False
