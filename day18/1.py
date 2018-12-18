#!/usr/bin/env python

import sys
from itertools import product
from collections import defaultdict

class Cell(object):
  def __init__(self, rep, pos):
    self.rep = rep
    self.pos = pos
    i, j = self.pos
    self.next = self.rep
    adj_pos = product([-1,0,1], repeat=2)
    self.adj = [ (i+ci, j+cj) for ci,cj in adj_pos if i+ci >= 0
                                                      and i+ci < worldx
                                                      and j+cj >= 0
                                                      and j+cj < worldy
                                                      and (i+ci,j+cj) != self.pos ]
    self.adj_num = defaultdict(lambda: 0)
  def __repr__(self):
    return self.rep
  def calc_next(self):
    if self.rep == '.':
      self.next = '|' if self.adj_num['|'] >= 3 else self.rep
    elif self.rep == '|':
      self.next = '#' if self.adj_num['#'] >= 3 else self.rep
    elif self.rep == '#':
      self.next = '#' if self.adj_num['#'] >= 1 and self.adj_num['|'] >= 1 else '.'

lines = []
with open(sys.argv[1]) as f:
  for line in f.readlines():
    lines += [ line.strip() ]

world = [ [ None for j in xrange(len(lines)) ] for i in xrange(len(lines[0])) ]
worldx = len(world[0])
worldy = len(world)
for i in xrange(worldx):
  for j in xrange(worldy):
    world[i][j] = Cell(lines[j][i], (i,j))
for i in xrange(worldx):
  for j in xrange(worldy):
    for ai,aj in world[i][j].adj:
      world[ai][aj].adj_num[ world[i][j].rep ] += 1
world_cache = defaultdict(lambda: None)

def cache(worldstream_rep, worldstream_next, minute):
  world_cache[ worldstream_rep ] = (worldstream_next, minute)

def fromcache(worldstream_rep):
  return world_cache[ worldstream_rep ]

def print_world(worldstream, minute):
  print
  print "After %d minutes: " % minute
  print "   %s" % ''.join([ str(" " if e < 10 else e/10 ) for e in xrange(worldx) ])
  print "   %s" % ''.join([ str(e % 10) for e in xrange(worldx) ])
  print
  for j in xrange(worldy):
    print "%2d %s" % (j, ''.join([ c for c in worldstream[j*worldy:(j+1)*worldy] ]))



def calc_nexts():
  for i in xrange(worldx):
    for j in xrange(worldy):
      world[i][j].calc_next()

def recalc_nums():
  for i in xrange(worldx):
    for j in xrange(worldy):
      c = world[i][j]
      if c.rep != c.next:
        for ai,aj in c.adj:
          world[ai][aj].adj_num[c.rep] -= 1
          world[ai][aj].adj_num[c.next] += 1

def set_rep2next():
  for i in xrange(worldx):
    for j in xrange(worldy):
      c = world[i][j]
      if c.rep != c.next:
        c.rep = c.next



minute = 0
worldstream_rep = ''.join( [c.rep for innerlist in world for c in innerlist] )
print_world(worldstream_rep, minute)
maxmin = int(sys.argv[2])
while minute < maxmin:
  worldstream_rep = ''.join( [c.rep for innerlist in world for c in innerlist] )

  if fromcache(worldstream_rep) is not None:
    break
  calc_nexts()
  worldstream_next = ''.join( [c.next for innerlist in world for c in innerlist] )
  cache(worldstream_rep, worldstream_next, minute)
  recalc_nums()
  set_rep2next()
  minute += 1

worldstream_rep, m = fromcache(worldstream_rep)
print "Breaking out at minute %d as it is the same as minute %d" % (minute, m)
cyclelength = minute-m
print "Cyclelength=%d" % cyclelength


minute += ( ( (maxmin - minute)/cyclelength ) * cyclelength )
minute += 1


while minute < maxmin:
  worldstream_rep,m = fromcache(worldstream_rep)
  minute += 1


print_world(worldstream_rep, minute)
wooden = worldstream_rep.count('|')
print "Wooden acres: %d" % wooden
lumberyards = worldstream_rep.count('#')
print "Lumberyard acres: %d" % lumberyards
print wooden*lumberyards
