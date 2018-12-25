#!/usr/bin/env python

import sys
from collections import deque
from itertools import combinations
import time

points = []
with open(sys.argv[1]) as f:
  for line in f.readlines():
    a,b,c,d = [ int(c) for c in line.strip().split(',') ]
    points += [ (a,b,c,d) ]

print "Read in %d points" % len(points)

class Constellation(object):
  def __init__(self, point):
    self.points = [ point ]

def distance( (a1,b1,c1,d1), (a2,b2,c2,d2) ):
  return abs(a1-a2) + abs(b1-b2) + abs(c1-c2) + abs(d1-d2)

consts = deque([])
for p in points:
  consts += [ Constellation(p) ]

def combine2const(c1, c2):
  for p1 in c1.points:
    for p2 in c2.points:
      yield (p1, p2)

def print_consts():
  print "Constellations: "
  print '\n'.join([ "%4d: %s" % (i+1, str(c.points)) for i,c in enumerate(consts) ])
  print

keepdoing = True
while keepdoing:
  #print_consts()
  print "Number of constellations: %d" % len(consts)
  keepdoing = False
  idx1 = 0
  while idx1 < len(consts):
    c1 = consts[idx1]
    for idx2,c2 in enumerate(consts):
      if idx1 >= idx2:
        continue
      if any([ distance(p1,p2) <= 3 for (p1,p2) in combine2const(c1, c2)  ]):
        c2.points += c1.points
        consts.remove(c1)
        keepdoing = True
        break
    idx1 += 1
    
  #time.sleep(0.1)


