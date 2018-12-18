#!/usr/bin/env python

import sys

class Node(object):
  def __init__(self, children, meta):
    self.children = children
    self.metadata = meta

data = None
with open(sys.argv[1]) as f:
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


def summeta(node, accu):
  sumchild = 0
  for ch in node.children:
    sumchild += summeta(ch, 0)
  return sumchild + sum([ int(m) for m in node.metadata ])


print "Sum of all metadata values: %d" % summeta(root, 0)
