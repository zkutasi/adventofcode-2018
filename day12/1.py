#!/usr/bin/env python

from collections import deque
import re
import sys

rgx_rule = re.compile('^(.*)\s+=>\s+(.*)$')

class Pot(object):
  def __init__(self, number, hasplantstr):
    self.number = number
    self.hasplant = hasplant(hasplantstr)
    self.willhaveplant = self.hasplant
  def __repr__(self):
    return '#' if self.hasplant else '.'

def hasplant(s):
  return True if s == '#' else False

rules = []
plantstate = None
with open(sys.argv[1]) as f:
  for line in [ l.strip() for l in f.readlines() ]:
    if line.startswith('initial state'):
      plantstate = deque([ Pot(i,p) for i,p in enumerate(line.split(':')[1].strip()) ])
    elif '=>' in line:
      rules += [ rgx_rule.split(line)[1:-1] ]

print rules

def print_state(g):
  print "Generation %2d: %s" % (g, ''.join([ ('#' if p.hasplant else '.') for p in plantstate ]))

g = 0
gmax = int(sys.argv[2])
while g<gmax:
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
      if [ p[1].hasplant for p in fivepots] == [ hasplant(elem) for elem in r[0] ]:
        #print "Rule matches: %r, fivepots: %s" % (r, fivepots)
        fivepots[2][1].willhaveplant = hasplant(r[1])
        if fivepots[2][0] == 'L' and fivepots[2][1].willhaveplant:
          if fivepots[3][0] == 'L':
            plantstate.appendleft(fivepots[3][1])
          plantstate.appendleft(fivepots[2][1])
        if fivepots[2][0] == 'R' and fivepots[2][1].willhaveplant:
          if fivepots[1][0] == 'R':
            plantstate.append(fivepots[1][1])
          plantstate.append(fivepots[2][1])
  for p in plantstate:
    p.hasplant = p.willhaveplant
  g += 1

print_state(g)
print "The sum of pot numbers that contain a plant: %d" % sum([ p.number for p in plantstate if p.hasplant ])
