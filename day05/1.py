#!/usr/bin/env python

def reacts(u1, u2):
  if u1 != u2 and u1.lower() == u2.lower():
    return True
  return False

first = None
size = 0
class Elem(object):
  def __init__(self, unit, prev, next):
    self.unit = unit
    self.prev = prev
    if prev is not None:
      prev.next = self
    self.next = next
    if next is not None:
      next.prev = self

with open('input.txt') as f:
  for line in f.readlines():
    prev = None
    for c in line.strip():
      e = Elem(c, prev, None)
      prev = e
      size += 1
      if first is None:
        first = e
  #print "Test the traversal"
  #curr = first
  #size_test = 0
  #while curr.next is not None:
  #  size_test += 1
  #  print "%s - %d" % (curr.unit, size_test)
  #  curr = curr.next
  print "The size of the polymer is %d" % size
  shrunk = True
  while shrunk:
    shrunk = False
    curr = first
    while curr.next is not None:
      if reacts(curr.unit, curr.next.unit):
        if curr.prev is None:
          print "We are at the front..."
          curr = curr.next.next
          first = curr
          curr.prev = None
        elif curr.next.next is None:
          print "We are almost at the very end"
          curr.prev.next = None
          curr = prev
        else:
          print "We are somewhere in the middle"
          curr.prev.next = curr.next.next
          curr.next.next.prev = curr.prev
          curr = curr.next.next
        shrunk = True
        size -= 2
        print "Size is %d" % size
      else:
        curr = curr.next
        #print "Step one ahead... %s" % curr.unit

print "Final size is %d" % size
