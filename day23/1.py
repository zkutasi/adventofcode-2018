#!/usr/bin/env python

import sys
import re

rgx = re.compile('^pos=<(\S+),(\S+),(\S+)>, r=(\S+)$')

class Nanobot(object):
  def __init__(self, x, y, z, r):
    self.x = x
    self.y = y
    self.z = z
    self.r = r
  def __repr__(self):
    return "pos=<%s,%s,%s>, r=%s" % (self.x, self.y, self.z, self.r)

nanobots = []
with open(sys.argv[1]) as f:
  for line in f.readlines():
    x,y,z,r = [ int(w) for w in rgx.split(line)[1:-1] ]
    nanobots += [ Nanobot(x,y,z,r) ]

def get_strongest():
  return max([ n for n in nanobots ], key=lambda n: n.r)

def get_distance(n1, n2):
  return abs(n1.x-n2.x) + abs(n1.y-n2.y) + abs(n1.z-n2.z)

strongest = get_strongest()
print "Strongest nanobot is %s" % strongest
print "In range with it are %d nanobots" % len([ n for n in nanobots if get_distance(n, strongest) <= strongest.r ])
