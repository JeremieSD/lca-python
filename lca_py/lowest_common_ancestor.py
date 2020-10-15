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

def main():
  root = setup()
  lca = findLCA(root,'j','o') #Change this to whichever letters from the binary_tree file to get another LCA
  if (lca is not -1):
    print(lca + " is the lowest common ancestor.")
  else:
    print('Lowest common ancestor cannot be found.')


if __name__ == "__main__":
    main()