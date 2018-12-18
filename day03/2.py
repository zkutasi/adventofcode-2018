#!/usr/bin/env python

import re
import sys

rgx = re.compile('#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')

class Claim(object):
  def __init__(self, s):
    ( self.id,
      self.fromleft,
      self.fromtop,
      self.width,
      self.height ) = rgx.split(s)[1:-1]
    self.id = int(self.id)
    self.fromleft = int(self.fromleft)
    self.fromtop = int(self.fromtop)
    self.width = int(self.width)
    self.height = int(self.height)
    self.overlaps = []
  def add_overlap_claim(self, c2):
    if c2.id not in self.overlaps:
      self.overlaps += [c2.id]

claims = []
with open(sys.argv[1]) as f:
  width = 0
  height = 0
  for line in f.readlines():
    claim = Claim(line)
    claims += [claim]
    if claim.fromleft + claim.width > width:
      width = claim.fromleft + claim.width
    if claim.fromtop + claim.height > height:
      height = claim.fromtop + claim.height
  print "It seems the size of the tunika is %dx%d" % (width, height)

  matrix = [ [ [] for x in range(width) ] for y in range(height) ]
  for c in claims:
    for w in range(c.width):
      for h in range(c.height):
        elem = matrix[h+c.fromtop][w+c.fromleft]
        for cc in elem:
          cc.add_overlap_claim(c)
          c.add_overlap_claim(cc)
        elem += [c]
  print "Finished marking the tunika..."
  for c in claims:
    if len(c.overlaps) == 0:
      print "The non-overlapping claim is: %d" % c.id
