#!/usr/bin/env python

import sys

depth = None
world = None
target_pos = None
with open(sys.argv[1]) as f:
  for line in f.readlines():
    if line.startswith('depth'):
      depth = int(line.strip().split()[1])
      world = [ [ None for y in xrange(depth) ] for x in xrange(depth) ]
    elif line.startswith('target'):
      target_pos = [ int(n) for n in line.strip().split()[1].split(',') ]

class Cell(object):
  def __init__(self, x, y):
    self.geoidx = None
    self.erolvl = None
    self.type = None
    self.risk = None
  def get_geoidx(self):
    if self.geoidx is None:
      if x == 0 and y == 0:
        geoidx = 0
      elif x == target_pos[0] and y == target_pos[1]:
        geoidx = 0
      elif y == 0:
        geoidx = x * 16807
      elif x == 0:
        geoidx = y * 48271
      else:
        geoidx = world[x-1][y].get_erolvl() * world[x][y-1].get_erolvl()
      self.geoidx = geoidx
    return self.geoidx
  def get_erolvl(self):
    if self.erolvl is None:
      self.erolvl = (self.get_geoidx() + depth) % 20183
    return self.erolvl
  def get_type(self):
    if self.type is None:
      self.get_erolvl()
      if self.erolvl % 3 == 0: # Rocky
        self.type = '.'
        self.risk = 0
      elif self.erolvl % 3 == 1: # Wet
        self.type = '='
        self.risk = 1
      else: # Narrow
        self.type = '|'
        self.risk = 2
    return self.type
  def __repr__(self):
    return self.get_type()

def print_world():
  maxdepth = 16
  for y in xrange(maxdepth):
    print ''.join([ str(world[x][y]) for x in xrange(maxdepth) ])

for x in xrange(target_pos[0]+1):
  for y in xrange(target_pos[1]+1):
    world[x][y] = Cell(x,y)
    world[x][y].get_type()

#print_world()
print sum([ world[x][y].risk for x in xrange(target_pos[0]+1) for y in xrange(target_pos[1]+1) ])
