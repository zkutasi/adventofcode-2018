#!/usr/bin/env python

import sys
import re
from math import floor
from collections import deque
import time

rgx = re.compile('^(x|y)=(\d+), (x|y)=(\d+)\.\.(\d+)$')
screenx = 200
screeny = 1800


scans = []
with open(sys.argv[1]) as f:
  for line in f.readlines():
    splittedline = rgx.split(line)[1:-1]
    if line.startswith('x'):
      x = ( int(splittedline[1]), int(splittedline[1]) )
      y = ( int(splittedline[3]), int(splittedline[4]) )
    else:
      y = ( int(splittedline[1]), int(splittedline[1]) )
      x = ( int(splittedline[3]), int(splittedline[4]) )
    scans += [ (x,y) ]

minx = min(scans, key=lambda ((x1,x2), (y1,y2)): x1)
minx = minx[0][0]
minx -= 1
maxx = max(scans, key=lambda ((x1,x2), (y1,y2)): x2)
maxx = maxx[0][1]
maxx += 1
miny = min(scans, key=lambda ((x1,x2), (y1,y2)): y1)
miny = miny[1][0]
miny_orig = miny
miny = 0
maxy = max(scans, key=lambda ((x1,x2), (y1,y2)): y2)
maxy = maxy[1][1]
print "minx=%d, maxx=%d, miny=%d, maxy=%d, dx=%d, dy=%d" % (minx,maxx,miny,maxy, maxx-minx, maxy-miny)

class Cell(object):
  def __init__(self, rep):
    self.rep = rep

world = [ [ Cell('.') for j in xrange(maxy+1) ] for i in xrange(maxx+1) ]
for s in scans:
  for x in xrange(s[0][0], s[0][1] + 1):
    for y in xrange(s[1][0], s[1][1] + 1):
      world[x][y].rep = '#'
spring_x = 500
world[spring_x][0].rep = '+'

def print_world():
  screen = [ [ ' ' for j in xrange(screeny) ] for i in xrange(screenx) ]
  #print "Screen size: %dx%d" % (len(screen), len(screen[0]) )
  for x in xrange(len(world)):
    for y in xrange(len(world[0])):
      if world[x][y].rep in ('#', '+', '|', '~'):
        x_onscreen = x - spring_x + screenx/2
        y_onscreen = y - miny
        if x_onscreen>=0 and x_onscreen < len(screen) and y_onscreen>=0 and y_onscreen < len(screen[0]):
          screen[x_onscreen][y_onscreen] = world[x][y].rep

  for y in xrange(len(screen[0])):
    print ''.join([ screen[i][y] for i in xrange(len(screen)) ])
  print

def create_pond(x,y):
  pxa = x
  pxb = x
  while world[pxa-1][y].rep in ('|'):
    pxa -= 1
  while world[pxb+1][y].rep in ('|'):
    pxb += 1
  if world[pxa-1][y].rep in ('#') and world[pxb+1][y].rep in ('#'):
    for xx in xrange(pxa, pxb+1):
      world[xx][y].rep = '~'
    return (True, (pxa, pxb))
  return (False, (0,0))

#print_world()

queue = deque([ (spring_x, 0, 'down') ])
while len(queue) > 0:
  x, y, direction = queue.popleft()
  #print x,y, len(queue)
  up = world[x][y-1]
  down = world[x][y+1] if y+1 < len(world[0]) else Cell('X')
  left = world[x-1][y]
  right = world[x+1][y] if x+1 < len(world) else Cell('X')
  if down.rep in ('.', '|'):
    down.rep = '|'
    queue.append( (x,y+1, 'down') )
  elif down.rep in ('#', '~'):
    if right.rep in ('.', '|') or left.rep in ('.', '|'):
      if right.rep in ('.', '|') and direction in ('right', 'down', 'up'):
        right.rep = '|'
        queue.append( (x+1,y, 'right') )
      if left.rep in ('.', '|') and direction in ('left', 'down', 'up'):
        left.rep = '|'
        queue.append( (x-1,y, 'left') )
    pondcreated, (pondxa, pondxb) = create_pond(x,y)
    if pondcreated:
      for xx in xrange(pondxa, pondxb+1):
        if world[xx][y-1].rep in ('|'):
          world[xx][y-1].rep = '|'
          queue.append( (xx, y-1, 'up') )
  #print_world()
  #time.sleep(0.1)

print_world()
print "Water tiles: %d" % (len([ cell for innerlist in world for cell in innerlist if cell.rep in ('|', '~') ]) - miny_orig + 1)
print "water in ponds %d" % len([ cell for innerlist in world for cell in innerlist if cell.rep in ('~') ])
