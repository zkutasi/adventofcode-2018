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
    self.area = 0
    self.is_edge = False

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
with open('input.txt') as f:
  for idx, line in enumerate(f.readlines()):
    x, y = [ int(c.strip()) for c in line.split(',') ]
    l = Loc(x, y, idx)
    locations += [l]

shrink = 15
test_world = [ ['..' for x in range(world_size/shrink+1)] for y in range(world_size/shrink+1)]
print_test_world(test_world)

enum_locs = zip(range(len(locations)), locations)
for x in range(world_size):
  progress("Calculating area for (%4d,%4d)" % (x, y))
  for y in range(world_size):
    curr = Loc(x,y)
    manhs = [ (idx, manhattan_dist(curr, loc)) for (idx, loc) in enum_locs ]
    minman = min(manhs, key=lambda (idx, manh): manh)
    idx, value = minman
    if zip(*manhs)[1].count(value) > 1:
      test_world[x/shrink][y/shrink] = '**'
      pass
    else:
      locations[idx].area +=1
      test_world[x/shrink][y/shrink] = "%2d" % idx
      if x==0 or y ==0 or x == world_size-1 or y == world_size-1:
        locations[idx].is_edge = True
      
print_test_world(test_world)



for l in locations:
  print "Area for location %2d (%4d,%4d): %10d %s" % (l.id, l.x, l.y, l.area, "EDGE" if l.is_edge else "")
