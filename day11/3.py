#!/usr/bin/env python

import sys
from collections import defaultdict

serialnum = int(sys.argv[1])

def progress(s):
  sys.stdout.write("%s\r" % s)
  sys.stdout.flush()

class Cell(object):
  def __init__(self, i, j):
    self.pos = (i+1,j+1)
    self.rackid = self.pos[0]+10
    self.powerlevel = self.rackid * self.pos[1]
    self.powerlevel += serialnum
    self.powerlevel *= self.rackid
    self.powerlevel = 0 if abs(self.powerlevel) < 100 else int(str(abs(self.powerlevel))[-3])
    self.powerlevel -= 5
  def __repr__(self):
    return str(self.powerlevel)

grid = [ [ Cell(i,j) for j in range(300) ] for i in range(300) ]
cache = {}
for s in range(len(grid)+1):
  cache[s] = defaultdict(lambda: None)

def sumsxs(x,y,s):
  summa = cache[s][(x-1,y)]
  if summa is not None:
    summa += sum([ cell.powerlevel for cell in grid[x+s-1][y:y+s] ])
    summa -= sum([ cell.powerlevel for cell in grid[x-1][y:y+s] ])
  else:
    summa = sum([ cell.powerlevel for innerlist in grid[x:x+s] for cell in innerlist[y:y+s] ])
  cache[s][(x,y)] = summa
  return summa

tops = []
for s in range(3,len(grid)):
  progress("Calculating for size=%d" % s)
  topsxs = max([ ((x+1,y+1,s), sumsxs(x,y,s)) for x in xrange(len(grid)-s) for y in xrange(len(grid[0])-s) ], key=lambda (pos, val): val)
  tops += [topsxs]

print "The top sxsxs square's is %s with power %d" % max(tops, key=lambda (pos, val): val)
