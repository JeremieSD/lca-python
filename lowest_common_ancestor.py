import unittest
from unittest.case import TestCase
#IMPORTANT NOTICE: Binary tree will not include duplicates. -> assumption made
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
            

def setup():
  file = open("binary_tree.txt","r")
  stringTree = file.read()
  rootNode = Node(stringTree[0])
  for x in stringTree:
    if (x is not " "):
      rootNode.insert(x)
  file.close()
  return rootNode

def findLCA(root,x,y):
  if (x is None or y is None or root is None):
    return -1
  vector1 = root.familyVector(x)
  vector2 = root.familyVector(y)
  print(vector1)
  print(vector2)
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
  def test_cases(self):
    lca = setup()
    self.assertEqual(findLCA(None,'k','e'),-1,msg="Null is good")
    self.assertEqual(findLCA(lca,'w','k'),'w',msg="Correct Root, w k")
    self.assertEqual(findLCA(lca,'z','g'),'w',msg="Correct lca z g")
    self.assertNotEqual(findLCA(lca,'a','l'),'a',msg='Correct invalid solution')
    self.assertEqual(findLCA(lca,'v','c'),'e',msg="Correct lca v c")

if __name__ == "__main__":
  unittest.main()