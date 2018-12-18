#!/usr/bin/env python

class Node(object):
  def __init__(self, children, meta):
    self.children = children
    self.metadata = meta
  def getvalue(self):
    if len(self.children) == 0:
      return sum([ int(m) for m in self.metadata ])
    else:
      value = 0
      for idx in [ int(i) for i in self.metadata ]:
        if idx == 0:
          pass
        elif idx > len(self.children):
          pass
        else:
          value += self.children[idx-1].getvalue()
      return value

data = None
with open('input.txt') as f:
  for line in f.readlines():
    data = line.split()
    break

def process_data(data, pos):
  numofchildren = int(data[pos])
  pos += 1
  numofmetadata = int(data[pos])
  pos += 1
  children = []
  for child in range(numofchildren):
    (newchild, pos) = process_data(data, pos)
    children += [newchild]
  meta = data[pos:pos+numofmetadata]
  pos += numofmetadata
  return (Node(children, meta), pos)

(root, _) = process_data(data, 0)


print "Value of root Node is: %d" % root.getvalue()
