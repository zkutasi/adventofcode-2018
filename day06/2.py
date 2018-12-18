#!/usr/bin/env python

import sys

def progress(s):
  sys.stdout.write("%s\r" % s)
  sys.stdout.flush()

def manhattan_dist(a, b):
  ax, ay = a.x, a.y
  bx, by = b.x, b.y
  return abs(abs(ax-bx) + abs(ay-by))

class Loc(object):
  def __init__(self, x, y, id=None):
    self.x = int(x)
    self.y = int(y)
    self.id = id

def print_test_world(test_world):
  for l in locations:
    lx = l.x/shrink
    ly = l.y/shrink
    test_world[lx][ly] = "%2d" % l.id
  for line in test_world:
    print ''.join(['--+'] * (world_size/shrink))
    print '|'.join(line)
  print
  print

world_size = 500
locations = []
with open(sys.argv[1]) as f:
  for idx, line in enumerate(f.readlines()):
    x, y = [ int(c.strip()) for c in line.split(',') ]
    l = Loc(x, y, idx)
    locations += [l]

shrink = 15
test_world = [ ['..' for x in range(world_size/shrink+1)] for y in range(world_size/shrink+1)]
print_test_world(test_world)

maxxum = 10000
safearea = 0
enum_locs = zip(range(len(locations)), locations)
for x in range(world_size):
  progress("Calculating for (%4d,%4d)" % (x, y))
  for y in range(world_size):
    curr = Loc(x,y)
    manhs = [ manhattan_dist(curr, loc) for (idx, loc) in enum_locs ]
    summan = sum(manhs)
    if summan < maxxum:
      safearea += 1
      test_world[x/shrink][y/shrink] = '##'
      
print_test_world(test_world)

print "Safe area: %d" % safearea
