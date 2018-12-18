#!/usr/bin/env python

import sys

serialnum = int(sys.argv[1])

class Cell(object):
  def __init__(self, i, j, debug=False):
    self.pos = (i+1,j+1)
    self.rackid = self.pos[0]+10
    self.powerlevel = self.rackid * self.pos[1]
    if debug:
      print self.powerlevel
    self.powerlevel += serialnum
    if debug:
      print self.powerlevel
    self.powerlevel *= self.rackid
    if debug:
      print self.powerlevel
    self.powerlevel = 0 if abs(self.powerlevel) < 100 else int(str(abs(self.powerlevel))[-3])
    if debug:
      print self.powerlevel
    self.powerlevel -= 5
    if debug:
      print self.powerlevel
  def __repr__(self):
    return str(self.powerlevel)

grid = [ [ Cell(i,j) for j in range(300) ] for i in range(300) ]

def sum3x3(x,y):
  summa = 0
  for i in range(x, x+3):
    for j in range(y, y+3):
      summa += grid[i][j].powerlevel
  return summa

def print3x3((x,y)):
  for i in range(x-1, x+3+1):
    output = ""
    for j in range(y-1, y+3+1):
      output += "%2s " % grid[i][j]
    print output

#print "Test: %s --> %s" % ((3,5), str(Cell(3,5, True)))
#print "Test: %s --> %s" % ((122,79), str(Cell(122,79, True)))
#print "Test: %s --> %s" % ((217,196), str(Cell(217,196, True)))
#print "Test: %s --> %s" % ((101,153), str(Cell(101,153, True)))
#sys.exit(1)

top3x3 = max([ (x+1,y+1, sum3x3(x,y)) for x in range(len(grid)-2) for y in range(len(grid[0])-2) ], key=lambda (pos, val): val)
print "The top 3x3 square's is %s with power %d" % top3x3
print "The grid around there is:"
print3x3(top3x3[0])
