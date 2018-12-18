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

  matrix = [ [ 0 for x in range(width) ] for y in range(height) ]
  for c in claims:
    for w in range(c.width):
      for h in range(c.height):
        matrix[h+c.fromtop][w+c.fromleft] += 1
  print "Finished marking the tunika..."
  count = 0
  for w in range(width):
    for h in range(height):
      if matrix[h][w] > 1:
        count += 1
  print "Multiclaim pieces: %d" % count
