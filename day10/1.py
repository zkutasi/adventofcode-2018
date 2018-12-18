#!/usr/bin/env python

import re
import time
import sys

rgx = re.compile('position=<(.+),(.+)> velocity=<(.+),(.+)>')
screensize_x = 90
screensize_y = 45

class Point(object):
  def __init__(self, pos, vel):
    self.pos = pos
    self.vel = vel
  def move(self):
    self.pos = (self.pos[0]+self.vel[0], self.pos[1]+self.vel[1])
  def __repr__(self):
    return "p:<%s>, v:<%s>" % (self.pos, self.vel)

def print_test_world():
  p_upmost = max(points, key=lambda p: p.pos[1])
  p_downmost = min(points, key=lambda p: p.pos[1])
  p_rightmost = max(points, key=lambda p: p.pos[0])
  p_leftmost = min(points, key=lambda p: p.pos[0])
  world_x0 = p_leftmost.pos[0]
  world_y0 = p_upmost.pos[1]
  world_size_x = abs(p_rightmost.pos[0]-p_leftmost.pos[0])
  world_size_y = abs(p_upmost.pos[1]-p_downmost.pos[1])
  shrink = 1
  if world_size_x > screensize_x or world_size_y > screensize_y:
    shrink_x = world_size_x/float(screensize_x) + 1
    shrink_y = world_size_y/float(screensize_y) + 1
    ar_screen = screensize_x/float(screensize_y)
    ar_world = world_size_x/float(world_size_y)
    if ar_screen > ar_world:
      shrink = shrink_y
    else:
      shrink = shrink_x
  print "World-size: %dx%d, shrink: %f" % (world_size_x, world_size_y, shrink)
  test_world = [ ['.' for x in range(screensize_x+1)] for y in range(screensize_y+1)]
  for p in points:
    px = int((p.pos[0] - world_x0)/shrink)
    py = int((p.pos[1] - world_y0)/shrink) + screensize_y
    if p in [p_upmost, p_downmost, p_leftmost, p_rightmost]:
      print "Borderpoint: %s,%s ---> %s,%s" % (p.pos[0], p.pos[1], px, py)
  for p in points:
    px = int((p.pos[0] - world_x0)/shrink)
    py = int((p.pos[1] - world_y0)/shrink) + screensize_y
    try:
      test_world[py][px] = "#"
    except IndexError:
      print "ERROR: %s,%s ---> %s,%s" % (p.pos[0], p.pos[1], px, py)
      sys.exit(1)
  for line in test_world:
    print ''.join(line)
  print
  print



points = []
with open(sys.argv[1]) as f:
  for line in f.readlines():
    px,py, vx,vy = rgx.split(line)[1:-1]
    points.append( Point( (int(px),int(py)), (int(vx),int(vy)) ) )
print "Number of points: %d" % len(points)



print_test_world()
step = 1
skipupfront = 10000
for s in range(skipupfront):
  [ p.move() for p in points ]
  step += 1

skipevery = 1
while True:
  [ p.move() for p in points ]
  if step % skipevery == 0:
    print "Step %d" % step
    print_test_world()
    time.sleep(0.1)
  step += 1
  if step > 10227:
    break
