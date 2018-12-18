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
sat = summedareatable = [ [ grid[i][j].powerlevel for j in range(300) ] for i in range(300) ]
for j in xrange(len(sat)):
  for i in xrange(len(sat[0])):
     sat[i][j] = ((0 if j==0 else sat[i][j-1]) + 
                  (0 if i==0 else sat[i-1][j]) -
                  (0 if i==0 or j==0 else sat[i-1][j-1]) +
                  sat[i][j])

def sumsxs(x,y,s):
  return sat[x][y] + sat[x+s][y+s] - sat[x][y+s] - sat[x+s][y]

tops = []
for s in range(2,len(grid)):
  progress("Calculating for size=%d" % s)
  topsxs = max([ ((x+1,y+1,s), sumsxs(x,y,s)) for x in xrange(len(grid)-s) for y in xrange(len(grid[0])-s) ], key=lambda (pos, val): val)
  tops += [topsxs]

print "The top sxsxs square's is %s with power %d" % max(tops, key=lambda (pos, val): val)
