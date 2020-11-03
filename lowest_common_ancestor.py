import unittest
from unittest.case import TestCase
from collections import defaultdict

#IMPORTANT NOTICE: Binary tree will not include duplicates. -> assumption made
#Assumption that nodes won't be negative values (-1), easier to demonstrate
class DAG:
  def __init__(self):
    self.nodes = dict()         # {'A':[ parents = [], children = [], depth = 0]}
    self.root = None
  def get_nodes(self):
    return self.nodes
  def insert_node(self, node, parent, child):
    node = str(node)
    if (node not in self.nodes):
      values = [[],[],0,'white']
      self.nodes[node] = values
      if (parent != None):
        self.nodes[node][0].append(parent)
        self.nodes[node][2] = self.nodes[parent][2] + 1
      if (child != None):
        self.nodes[node][1].append(child)
      return True
    return False

  def add_edge(self, edge):
    parent = edge[0]
    child = edge[1]
    if child == '-':
      return
    if (not self.insert_node(parent, None, child)):
      if (child not in self.nodes[parent][1]):
        self.nodes[parent][1].append(child)
    if (not self.insert_node(child, parent, None)):
      if (parent not in self.nodes[child][0]):
        self.nodes[child][0].append(parent)

  def recursiveSearch(self, node, passed_set):
    passed_set.add(node)
    for parent in self.nodes[node][0]:
      passed_set.add(node)
      self.recursiveSearch(parent, passed_set)

  def findLCA(self, firstNode, secondNode):
    first_path_nodes = set()
    second_path_nodes = set()
    if (firstNode in self.nodes):
      self.recursiveSearch(firstNode, first_path_nodes)
    else:
      return -1
    if (secondNode in self.nodes):
      self.recursiveSearch(secondNode, second_path_nodes)
    else:
      return -1
    for node in first_path_nodes:
      self.nodes[node][3] = 'blue'
    for node in second_path_nodes:
      if self.nodes[node][3] is 'blue':
        self.nodes[node][3] = 'red'
    for node in self.nodes:
      if self.nodes[node][3] is 'red':
        for parent in self.nodes[node][0]:
          self.nodes[parent][2]+=1
    lca_node = -1
    for node in self.nodes:
      if self.nodes[node][3] is 'red' and self.nodes[node][2] is 0:
        lca_node = node
    for node in self.nodes:
      self.nodes[node][3] = 'white'
      self.nodes[node][2] = 0
    return lca_node

  def displayTable(self):
    for pair in self.nodes.items():
      print(pair)

class Node:
  def __init__(self, id):
    self.id = id
    self.childL = None
    self.childR = None

  def  insert(self,id):
    if self.id:
      if id < self.id:
        if self.childL is None:
          self.childL = Node(id)
        else:
          self.childL.insert(id)
      elif id > self.id:
        if self.childR is None:
          self.childR = Node(id)
        else:
          self.childR.insert(id)

  def familyVector(self,id):
    familyVector = []
    if id is self.id:
      return self.id
    else:
      familyVector.append(self.id)
      if id < self.id:
        if self.childL is None:
          return -1
        else:
          temp = (self.childL.familyVector(id))
          if (not isinstance(temp,str)):
            for x in temp:
             familyVector.append(x)
          else:
            familyVector.append(temp)
      elif id > self.id:
        if self.childR is None:
          return -1
        else:
          temp = (self.childR.familyVector(id))
          if (not isinstance(temp,str)):
            for x in temp:
             familyVector.append(x)
          else:
            familyVector.append(temp)
      return familyVector    
            

def setup(cyclic ,nameF): #Since the main part of the assignment is to test, all the graphs are practically predetermined, however files can be made for other graphs.
  if (cyclic == False):
    file = open(nameF,"r")
    stringTree = file.read()
    rootNode = Node(stringTree[0])
    for x in stringTree:
     if (x is not " "):
       rootNode.insert(x)
    file.close()
    return rootNode
  #graph taken from https://medium.com/kriptapp/guide-what-is-directed-acyclic-graph-364c04662609 (DAG)
  file = open(nameF, "r")
  dag = DAG()
  for index in file:
    index = index[:-1]
    dag.insert_node(index[0],None,None)
  file.close()
  file = open(nameF, "r")
  for index in file:
    index = index[:-1]
    values = index.split(':')
    key = values[0]
    val = values[1].split(',')
    for x,y in enumerate(val):
      dag.add_edge([key,y])
  file.close()
  return dag
  

def findLCA(root,x,y):
  if (x is None or y is None or root is None):
    return -1
  vector1 = root.familyVector(x)
  vector2 = root.familyVector(y)
  incrementer = 0
  while(vector1[incrementer] is vector2[incrementer] or vector1 is vector2[0] or vector2 is vector1 [0]):
    incrementer+=1
    if (incrementer >= (len(vector1) and len(vector2))):
      break
    elif (incrementer >= (len(vector1) or len(vector2))):
      break
  if (incrementer is not 0 and (vector1[-1] is not -1 and vector2[-1] is not -1)):
    incrementer-=1
    return vector1[incrementer]
  else:
    return -1
  
  
  
  

class UnitTestLCA(unittest.TestCase):
  def test_cases_binary(self):
    lca = setup(False,"binary_tree.txt")
    self.assertEqual(findLCA(None,'k','e'),-1,msg="Null is good")
    self.assertEqual(findLCA(lca,'w','k'),'w',msg="Correct Root, w k")
    self.assertEqual(findLCA(lca,'z','g'),'w',msg="Correct lca z g")
    self.assertNotEqual(findLCA(lca,'a','l'),'a',msg='Correct invalid solution')
    self.assertEqual(findLCA(lca,'v','c'),'e',msg="Correct lca v c")
  
  def test_cases_acyclic(self): #There can be more than one solution, only one of them is being used here however
    dga = setup(True,"acyclic_tree.txt")
    self.assertEqual(dga.findLCA('e','f'),'e',msg='Correct LCA e')
    self.assertEqual(dga.findLCA(None,'f'),-1,msg='None is good')
    self.assertEqual(dga.findLCA('a','g'),-1,msg='Correct LCA (no solution)')
    self.assertEqual(dga.findLCA('c','d'),'b',msg='Correct LCA b')
    self.assertEqual(dga.findLCA('a','b'),'a',msg='Correct LCA a')



if __name__ == "__main__":
  unittest.main()