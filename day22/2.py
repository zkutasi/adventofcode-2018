#!/usr/bin/env python

import sys
from collections import deque, defaultdict
import heapq
import time

depth = None
world = None
target_pos = None
with open(sys.argv[1]) as f:
  for line in f.readlines():
    if line.startswith('depth'):
      depth = int(line.strip().split()[1])
    elif line.startswith('target'):
      target_pos = [ int(n) for n in line.strip().split()[1].split(',') ]

boundary_x = min(150, depth)
boundary_y = min(1500, depth)
world = [ [ None for y in xrange(boundary_y) ] for x in xrange(boundary_x) ]

class Cell(object):
  def __init__(self, x, y):
    self.pos = [x,y]
    self.erolvl = None
    self.type = None
  def get_erolvl(self):
    def get_geoidx():
      if self.pos == [0,0]:
        geoidx = 0
      elif self.pos == target_pos:
        geoidx = 0
      elif self.pos[1] == 0:
        geoidx = self.pos[0] * 16807
      elif self.pos[0] == 0:
        geoidx = self.pos[1] * 48271
      else:
        geoidx = world[self.pos[0]-1][self.pos[1]].get_erolvl() * world[self.pos[0]][self.pos[1]-1].get_erolvl()
      return geoidx
    if self.erolvl is None:
      self.erolvl = (get_geoidx() + depth) % 20183
    return self.erolvl
  def get_type(self):
    if self.type is None:
      self.get_erolvl()
      if self.erolvl % 3 == 0: # Rocky
        self.type = '.'
      elif self.erolvl % 3 == 1: # Wet
        self.type = '='
      else: # Narrow
        self.type = '|'
    return self.type
  def __repr__(self):
    return "%s, %s" % (self.get_type(), self.pos)


tools = {
  'N': set(['=', '|']),
  'T': set(['.', '|']),
  'C': set(['.', '='])
}

types = {
   '.': set(['C', 'T']),
   '=': set(['C', 'N']),
   '|': set(['T', 'N'])
}

print "Building graph for problem..."
for x in xrange(boundary_x):
  for y in xrange(boundary_y):
    world[x][y] = Cell(x,y)
    #world[x][y].get_type()
print "Graph built..."

def get_adjs(node, curr_tool):
  x, y = node.pos
  curr_type = world[x][y].get_type()
  if x > 0:
    next_type = world[x-1][y].get_type()
    if curr_type == next_type or tools[curr_tool] == set([curr_type, next_type]):
      yield (world[x-1][y], 1, curr_tool)
    else:
      new_tool = (t for t in types[curr_type] if t != curr_tool).next()
      yield (world[x-1][y], 8, new_tool)
  if x < boundary_x-1:
    next_type = world[x+1][y].get_type()
    if curr_type == next_type or tools[curr_tool] == set([curr_type, next_type]):
      yield (world[x+1][y], 1, curr_tool)
    else:
      new_tool = (t for t in types[curr_type] if t != curr_tool).next()
      yield (world[x+1][y], 8, new_tool)
  if y > 0:
    next_type = world[x][y-1].get_type()
    if curr_type == next_type or tools[curr_tool] == set([curr_type, next_type]):
      yield (world[x][y-1], 1, curr_tool)
    else:
      new_tool = (t for t in types[curr_type] if t != curr_tool).next()
      yield (world[x][y-1], 8, new_tool)
  if y < boundary_y-1:
    next_type = world[x][y+1].get_type()
    if curr_type == next_type or tools[curr_tool] == set([curr_type, next_type]):
      yield (world[x][y+1], 1, curr_tool)
    else:
      new_tool = (t for t in types[curr_type] if t != curr_tool).next()
      yield (world[x][y+1], 8, new_tool)

def shortest_path_dijkstra(start, end, start_tool):
  queue = []
  distances = { (world[x][y], tool): float('infinity') for x in xrange(boundary_x)
                                                       for y in xrange(boundary_y)
                                                       for tool in tools.keys() }
  distances[ (start, start_tool) ] = 0


  heapq.heappush(queue, (0, start_tool, start))
  while queue:
    curr_dist, curr_tool, curr_node = heapq.heappop(queue)
    #print "Taking Node %s out, distance so far is %d, using tool %s" % (curr_node, curr_dist, curr_tool)
    #time.sleep(1)
    if curr_node == end:
      print "Fastest way to reach target so far is %s" % (distances[ (end, curr_tool) ] if curr_tool == 'T' else distances[ (end, curr_tool) ]+7)
    for neighbor, neighbor_dist, new_tool in get_adjs(curr_node, curr_tool):
      #print "Neighbor %s has dist of %d, using tool %s" % (neighbor, neighbor_dist, new_tool)
      distance = distances[ (curr_node, curr_tool) ] + neighbor_dist
      if distance < distances[(neighbor, new_tool) ]:
        #print "Distance became lower for %s: %d" % (neighbor, distance)
        distances[ (neighbor, new_tool) ] = distance
        heapq.heappush( queue, (distance, new_tool, neighbor) )

  return
        

sp = shortest_path_dijkstra( world[0][0], world[target_pos[0]][target_pos[1]], 'T' )


