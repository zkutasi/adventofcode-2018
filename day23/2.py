#!/usr/bin/env python

import sys
import re
from collections import deque
import time
import math

rgx = re.compile('^pos=<(\S+),(\S+),(\S+)>, r=(\S+)$')

class Nanobot(object):
  def __init__(self, x, y, z, r):
    self.pos = (x,y,z)
    self.r = r
  def __repr__(self):
    return "pos=%s, r=%s" % ("<%s,%s,%s>" % self.pos, self.r)

nanobots = []
with open(sys.argv[1]) as f:
  for line in f.readlines():
    x,y,z,r = [ int(w) for w in rgx.split(line)[1:-1] ]
    nanobots += [ Nanobot(x,y,z,r) ]
print "Read in %d nanobots" % len(nanobots)
#print nanobots



def get_world_size(nanobots):
  minx = min([ n.pos[0]-n.r for n in nanobots ])
  maxx = max([ n.pos[0]+n.r for n in nanobots ])
  miny = min([ n.pos[1]-n.r for n in nanobots ])
  maxy = max([ n.pos[1]+n.r for n in nanobots ])
  minz = min([ n.pos[2]-n.r for n in nanobots ])
  maxz = max([ n.pos[2]+n.r for n in nanobots ])
  minr = min([ n.r for n in nanobots ])
  maxr = max([ n.r for n in nanobots ])

  print "X = (%10d...%10d)" % (minx, maxx)
  print "Y = (%10d...%10d)" % (miny, maxy)
  print "Z = (%10d...%10d)" % (minz, maxz)
  print "R = (%10d...%10d)" % (minr, maxr)
  return minx,maxx, miny,maxy, minz,maxz

def get_distance( (x1,y1,z1) , (x2,y2,z2) ):
  return abs(x1-x2) + abs(y1-y2) + abs(z1-z2)
  

def howmany_inrange(x,y,z, nanobots):
  def is_inrange(n):
    return get_distance((x,y,z), n.pos) <= n.r

  count = 0
  for n in nanobots:
    if is_inrange(n):
      count += 1
  return count

wminx,wmaxx, wminy,wmaxy, wminz,wmaxz = get_world_size(nanobots)
scale_jumps = 10
scale_levels = max( [ int(math.log10(i)) for i in [abs(wminx-wmaxx), abs(wminy-wmaxy), abs(wminz-wmaxz)] ] )
scale = scale_jumps**scale_levels

def scan_scaled_regions(regions, scale):
  if scale > 1:
    scaled_nanobots = [ Nanobot(n.pos[0]/scale,
                                n.pos[1]/scale,
                                n.pos[2]/scale,
                                n.r/scale + 3) for n in nanobots ]
  else:
    scaled_nanobots = nanobots
  #print "Scaled nanobots:"
  #print '\n'.join([ str(n) for n in scaled_nanobots ])
  max_inrange = -1
  max_inrange_pos = set()
  n = 0
  for rstart,rend in regions:
    x1,y1,z1 = rstart
    x2,y2,z2 = rend
    x1s,y1s,z1s = [ c/scale for c in rstart ]
    x2s,y2s,z2s = [ c/scale+1 for c in rend ]
    print "Region %s---%s with scale: %d" % (str((x1s,y1s,z1s)), str((x2s,y2s,z2s)), scale)
    for x in xrange(x1s, x2s+1):
      for y in xrange(y1s, y2s+1):
        for z in xrange(z1s, z2s+1):
          inrange = howmany_inrange(x,y,z, scaled_nanobots)
          if inrange > max_inrange:
            max_inrange = inrange
            max_inrange_pos = set([ ((x*scale,y*scale,z*scale),((x+1)*scale,(y+1)*scale,(z+1)*scale)) ])
          elif inrange == max_inrange:
            max_inrange_pos.add( ((x*scale,y*scale,z*scale),((x+1)*scale,(y+1)*scale,(z+1)*scale)) )
    n += 1
    print "Max so far: %d @ %s regions (%d/%d)" % (max_inrange, len(max_inrange_pos), n, len(regions))
  return (max_inrange, max_inrange_pos)



max_inrange_pos = set([ ((wminx,wminy,wminz),(wmaxx,wmaxy,wmaxz)) ])
while scale > 0:
  print "Scale %d, Regions: %d" % (scale, len(max_inrange_pos))
  max_inrange, max_inrange_pos = scan_scaled_regions(max_inrange_pos, scale)
  scale /= scale_jumps

first_pos = list(max_inrange_pos)[0][0]
print "Maximum inrange nanobots: %4s @ positions %s, with manhattan dist %d" % (max_inrange, first_pos, sum(first_pos))
