#!/usr/bin/env python

def reacts(u1, u2):
  if u1 != u2 and u1.lower() == u2.lower():
    return True
  return False

def react_poly(poly):
  first = None
  size = 0
  prev = None
  for c in poly:
    e = Elem(c, prev, None)
    prev = e
    size += 1
    if first is None:
      first = e
  shrunk = True
  while shrunk:
    shrunk = False
    curr = first
    while curr.next is not None:
      if reacts(curr.unit, curr.next.unit):
        if curr.prev is None:
          #print "We are at the front..."
          curr = curr.next.next
          first = curr
          curr.prev = None
        elif curr.next.next is None:
          #print "We are almost at the very end"
          curr.prev.next = None
          curr = prev
        else:
          #print "We are somewhere in the middle"
          curr.prev.next = curr.next.next
          curr.next.next.prev = curr.prev
          curr = curr.next.next
        shrunk = True
        size -= 2
        #print "Size is %d" % size
      else:
        curr = curr.next
        #print "Step one ahead... %s" % curr.unit
  #print "Final size is %d" % size
  return size

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
  poly = f.readlines()[0].strip()
  print "The size of the polymer is %d" % len(poly)
  chars = ''.join(set(poly.lower()))
  min_size = None
  for c in chars:
    improved = poly.replace(c.lower(), '').replace(c.upper(), '')
    reacted_size = react_poly(improved)
    print "By removing character '%s' from polymer, size is: %s " % (c, reacted_size)
    if min_size is None:
      min_size = reacted_size
    elif reacted_size < min_size:
      min_size = reacted_size

print "The minimum reacted polymer size seems to be: %s" % min_size
