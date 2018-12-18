#!/usr/bin/env python

from collections import deque, defaultdict
import sys
import time

class CombatEnded(Exception):
  pass

class ElfDied(Exception):
  pass

class CaveElement(object):
  def __init__(self, pos):
    self.pos = pos
  def taketurn(self):
    raise NotImplementedError
  def move(self):
    raise NotImplementedError
  def attack(self):
    raise NotImplementedError
  def get_adjacents(self):
    adj = []
    adj += [ cave[self.pos[0]][self.pos[1]-1] ]
    adj += [ cave[self.pos[0]-1][self.pos[1]] ]
    adj += [ cave[self.pos[0]+1][self.pos[1]] ]
    adj += [ cave[self.pos[0]][self.pos[1]+1] ]
    return adj
  def enemiesinrange(self, enemy):
    return [ c for c in cave[self.pos[0]][self.pos[1]].get_adjacents()
             if isinstance(c, enemy)
             and not c.dead
           ]


class Ground(CaveElement):
  def __init__(self, pos):
    super(Ground, self).__init__(pos)
    self.rep = '.'
  def taketurn(self):
    pass
  def __repr__(self):
    return "%s%s" % (self.rep, str(self.pos))
    

class Wall(CaveElement):
  def __init__(self, pos):
    super(Wall, self).__init__(pos)
    self.rep = '#'
  def taketurn(self):
    pass
  def __repr__(self):
    return "%s%s" % (self.rep, str(self.pos))



maxhitpoints = 200
class Unit(CaveElement):
  def __init__(self, pos, enemy):
    super(Unit, self).__init__(pos)
    self.enemy = enemy
    self.hitpoints = maxhitpoints
    self.attackpower = 3
    self.dead = False
  def taketurn(self):
    if self.dead:
      return
    self.move()
    self.attack()
  def move(self):
    #print "Start: %s" % self
    if len([ cave[i][j]
             for i in xrange(cavex)
             for j in xrange(cavey)
             if isinstance(cave[i][j], self.enemy)
           ]) == 0:
      raise CombatEnded
    if len(self.enemiesinrange(self.enemy)) > 0:
      return
    inrange = sorted([
                 cave[i][j]
                 for i in xrange(cavex)
                 for j in xrange(cavey)
                 if isinstance(cave[i][j], Ground)
                 and len(cave[i][j].enemiesinrange(self.enemy)) > 0
               ], key=lambda cell: (cell.pos[1], cell.pos[0]))
    #print "Inrange-list: %s" % [ c for c in inrange ]
    if len(inrange) == 0:
      return
    reachable = deque([])
    for cell in inrange:
      try:
        sp = shortest_path_bfs(self, cell).next()
      except StopIteration:
        continue
      if len(reachable) == 0:
        reachable.append( (cell, sp) )
        continue
      if len(sp) <= len(reachable[0][1]):
        reachable.appendleft( (cell, sp) )
      else:
        reachable.append( (cell, sp) )
    #print "Reachable-list: %s" % [ c[0] for c in reachable ]
    if len(reachable) == 0:
      return
    nearest_value = len(reachable[0][1]) if len(reachable) > 0 else None
    nearest = deque([])
    for cell, sp in reachable:
      if len(sp) == nearest_value:
        nearest.appendleft( (cell,sp) )
      else:
        break
    #print "Nearest-list: %s" % [ c for c in nearest ]

    newpos = nearest[0][1][1]
    oldpos = self.pos
    self.pos = newpos
    cave[oldpos[0]][oldpos[1]] = Ground( (oldpos[0], oldpos[1]) )
    cave[newpos[0]][newpos[1]] = self
      
    #print "End: %s" % self
  def attack(self):
    enemiesinrange = self.enemiesinrange(self.enemy)
    if len(enemiesinrange) == 0:
      return
    enemy = min(enemiesinrange, key=lambda e: e.hitpoints)
    enemy.hitpoints -= self.attackpower
    if enemy.hitpoints <= 0:
      enemy.dead = True
      cave[enemy.pos[0]][enemy.pos[1]] = Ground( (enemy.pos[0],enemy.pos[1]) )
      if isinstance(enemy, Elf):
        raise ElfDied
      
  def __repr__(self):
    raise NotImplementedError


class Elf(Unit):
  def __init__(self, pos, elfpower=3):
    super(Elf, self).__init__(pos, Goblin)
    self.attackpower = elfpower
    self.rep = 'E'
  def __repr__(self):
    return "%s%s" % (self.rep, str(self.pos))


class Goblin(Unit):
  def __init__(self, pos):
    super(Goblin, self).__init__(pos, Elf)
    self.rep = 'G'
  def __repr__(self):
    return "%s%s" % (self.rep, str(self.pos))



def shortest_path_bfs(start, end):
  queue = deque([(start, [ start.pos ])])
  visited = defaultdict(lambda: False)
  visited[start.pos] = True
  while queue:
    (vertex, path) = queue.popleft()
    for node in [ v for v in vertex.get_adjacents() if isinstance(v, Ground) ]:
      #if node.pos in path:
      if visited[node.pos]:
        continue
      if node.pos == end.pos:
        yield path + [ node.pos ]
      else:
        queue.append((node, path + [ node.pos ]))
        visited[node.pos] = True

def print_cave(roundnum):
  print "Round %d:" % roundnum
  print "   %s" % ''.join([ str(" " if e < 10 else e/10 ) for e in xrange(cavex) ])
  print "   %s" % ''.join([ str(e % 10) for e in xrange(cavex) ])
  print
  for j in xrange(len(cave)):
    print "%2d %s   %s" % (j, ''.join([ cave[i][j].rep for i in xrange(cavex) ]),
                              ', '.join([ "%s(%d)" % (cave[i][j].rep, cave[i][j].hitpoints)
                                          for i in xrange(cavex)
                                          if isinstance(cave[i][j], Unit) ]))
  print


cave = None
cavex = 0
cavey = 0
units = None
def readinput(elfpower=3):
  global cave
  global cavex
  global cavey
  global units

  lines = []
  with open(sys.argv[1]) as f:
    for line in f.readlines():
      lines += [ line.replace('\n', '') ]

  cavex = len(lines[0])
  cavey = len(lines)
  cave = [ [ None for j in xrange(cavey) ] for i in xrange(cavex) ]
  units = []
  for i in xrange(cavex):
    for j in xrange(cavey):
      if lines[j][i] == '.':
        cave[i][j] = Ground( (i,j) )
      elif lines[j][i] == '#':
        cave[i][j] = Wall( (i,j) )
      elif lines[j][i] == 'E':
        unit = Elf( (i,j), elfpower=elfpower )
        cave[i][j] = unit
        units += [ unit ]
      elif lines[j][i] == 'G':
        unit = Goblin( (i,j) )
        cave[i][j] = unit
        units += [ unit ]




elfpower = 4
try:
  for p in xrange(elfpower, maxhitpoints):
    print "Using ElfPower %d..." % elfpower
    readinput(elfpower)
    roundnum = 0
    print_cave(roundnum)
    try:
      while True:
        for unit in sorted(units, key=lambda u: (u.pos[1], u.pos[0])):
          unit.taketurn()
        roundnum += 1
        print_cave(roundnum)
        time.sleep(0.2)
    except ElfDied:
      elfpower += 1
except CombatEnded:
  pass

print_cave(roundnum)
print roundnum * sum([ u.hitpoints for u in units if not u.dead ])


