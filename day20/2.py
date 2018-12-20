#!/usr/bin/env python

import sys
from collections import deque
from collections import defaultdict

def get_all_paths(r):
  all_paths = deque([])

  def inner(r_idx):
    path_alternatives = deque([""])
    while r[r_idx] not in (')', '$'):
      #print "Handling char %s" % r[r_idx]
      if r[r_idx] in ('('):
        r_idx, new_path_alternatives = inner(r_idx+1)

        pa = path_alternatives.pop()
        for npa in new_path_alternatives:
          path_alternatives.append(pa + npa)
        #print path_alternatives
      elif r[r_idx] in ('|'):
        path_alternatives.append("")
      else:
        path_alternatives[-1] += r[r_idx]
        #print path_alternatives

      r_idx += 1

    return (r_idx, deque(set(path_alternatives)))

  result = inner(1)[1]
  return result

class Room(object):
  def __init__(self, posx, posy):
    self.posx = posx
    self.posy = posy
    self.adj = set()
  def __repr__(self):
    return "(%s,%s)" % (self.posx, self.posy)

def print_world():
  min_room_x = min([ r.posx for r in rooms.values() ])
  min_room_y = min([ r.posy for r in rooms.values() ])
  max_room_x = max([ r.posx for r in rooms.values() ])
  max_room_y = max([ r.posy for r in rooms.values() ])
  world_x = max_room_x-min_room_x
  world_y = max_room_y-min_room_y
  print '#' * (2 * (max_room_x - min_room_x + 1) + 1)
  for y in xrange(min_room_y, max_room_y+1):
    print "#%s" % ''.join([ "%s%s" % ('X' if rooms[ (x,y) ].posx == 0 and rooms[ (x,y) ].posy == 0 else ' ',
                                      '|' if (x+1,y) in rooms and rooms[ (x+1,y) ] in rooms[ (x,y) ].adj else '#')
                            for x in xrange(min_room_x, max_room_x+1) ])
    print "#%s" % ''.join([ "%s%s" % ('-' if (x,y+1) in rooms and rooms[ (x,y+1) ] in rooms[ (x,y) ].adj else '#',
                                      '#')
                            for x in xrange(min_room_x, max_room_x+1) ])

def get_rooms(path_list):
  rooms = defaultdict(lambda: None)
  rooms[(0,0)] = Room(0,0)
  for p in path_list:
    #print "Traversing path %s" % p
    posx = 0
    posy = 0
    for c in p:
      room_from = rooms[(posx,posy)]
      if   c == 'W':
        posx -= 1
      elif c == 'E':
        posx += 1
      elif c == 'N':
        posy -= 1
      elif c == 'S':
        posy += 1
      room_to = rooms[(posx,posy)]
      if room_to is None:
        #print "Adding room: %s, direction is %s" % (str( (posx,posy) ), c)
        room_to = Room(posx, posy)
        rooms[ (posx,posy) ] = room_to
      room_to.adj.add( room_from )
      room_from.adj.add( room_to )
  return rooms

def shortest_path_bfs(start):
  shortest_paths = {}
  queue = deque([(start, [ start ])])
  visited = defaultdict(lambda: False)
  visited[start] = True
  while queue:
    (vertex, path) = queue.popleft()
    for node in vertex.adj:
      if visited[node]:
        continue
      if node not in shortest_paths:
        #print "Found shortest path %s-->%s" % (start, node)
        shortest_paths[node] = path + [ node ]
      queue.append((node, path + [ node ]))
      visited[node] = True
  return shortest_paths

with open(sys.argv[1]) as f:
  for line in f.readlines():
    rgx = line.strip()
    path_list = get_all_paths(rgx)
    rooms = get_rooms(path_list)
    print_world()
    print "Number of rooms: %d" % len(rooms)
    sps = shortest_path_bfs(rooms[(0,0)])

    print "Furthest room requires passing %d doors" % max([ len(sp[1:]) for to,sp in sps.items() ])
    print "Rooms with at least 1000 doors to pass is %d" % len([ to for to,sp in sps.items() if len(sp[1:]) >= 1000 ])

