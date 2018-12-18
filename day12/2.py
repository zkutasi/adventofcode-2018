#!/usr/bin/env python

from collections import deque
import re
import sys

rgx_rule = re.compile('^(.*)\s+=>\s+(.*)$')

class Pot(object):
  def __init__(self, number, hasplant):
    self.number = number
    self.hasplant = hasplant
    self.willhaveplant = self.hasplant
  def __repr__(self):
    return self.hasplant

rules = []
plantstate = None
with open(sys.argv[1]) as f:
  for line in [ l.strip() for l in f.readlines() ]:
    if line.startswith('initial state'):
      plantstate = deque([ Pot(i,p) for i,p in enumerate(line.split(':')[1].strip()) ])
    elif '=>' in line:
      rules += [ rgx_rule.split(line)[1:-1] ]

def print_state(g):
  print "Generation %2d: %s" % (g, ''.join([ str(p) for p in plantstate ]))

def plantstate_tostring(ps):
  return (''.join([ p.hasplant for p in ps ]), sum([ p.number for p in ps if p.hasplant == '#' ]))

g = 0
gmax = int(sys.argv[2])
prevplantstatestr = (None, None)
plantstatestr = plantstate_tostring(plantstate)
plantstatestrings = []
while g<gmax and not prevplantstatestr[0] == plantstatestr[0]:
  plantstatestrings += [ plantstatestr ]
  print_state(g)
  extended_pots = [ ('L', Pot(plantstate[0].number-4, '.')),
                    ('L', Pot(plantstate[0].number-3, '.')),
                    ('L', Pot(plantstate[0].number-2, '.')),
                    ('L', Pot(plantstate[0].number-1, '.')) ] + \
                  [ ('', p) for p in plantstate ] + \
                  [ ('R', Pot(plantstate[-1].number+1, '.')),
                    ('R', Pot(plantstate[-1].number+2, '.')),
                    ('R', Pot(plantstate[-1].number+3, '.')),
                    ('R', Pot(plantstate[-1].number+4, '.')) ]
  for r in rules:
    for fivepots in zip(
                   extended_pots,
                   extended_pots[1:],
                   extended_pots[2:],
                   extended_pots[3:],
                   extended_pots[4:]):
      if fivepots[0][1].hasplant == r[0][0] and \
         fivepots[1][1].hasplant == r[0][1] and \
         fivepots[2][1].hasplant == r[0][2] and \
         fivepots[3][1].hasplant == r[0][3] and \
         fivepots[4][1].hasplant == r[0][4]:
        #print "Rule matches: %r, fivepots: %s" % (r, fivepots)
        fivepots[2][1].willhaveplant = r[1]
        if fivepots[2][0] == 'L' and fivepots[2][1].willhaveplant == '#':
          if fivepots[3][0] == 'L':
            plantstate.appendleft(fivepots[3][1])
          plantstate.appendleft(fivepots[2][1])
        if fivepots[2][0] == 'R' and fivepots[2][1].willhaveplant == '#':
          if fivepots[1][0] == 'R':
            plantstate.append(fivepots[1][1])
          plantstate.append(fivepots[2][1])
  for p in plantstate:
    p.hasplant = p.willhaveplant
  while plantstate[0].willhaveplant == '.':
    plantstate.popleft()
  while plantstate[-1].willhaveplant == '.':
    plantstate.popright()
  g += 1
  prevplantstatestr = (plantstatestr[0], plantstatestr[1])
  plantstatestr = plantstate_tostring(plantstate)

plantstatestrings += [ plantstatestr ]

print "The processing until stable state finished. Current sum is: %d" % plantstatestrings[-1][1]

print plantstatestrings[-2:]

print "The sum of pot numbers that contain a plant: %d" % (plantstatestrings[-1][1] + (gmax-g)*(plantstatestrings[-1][1]-plantstatestrings[-2][1]))

