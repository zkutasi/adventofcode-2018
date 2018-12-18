#!/usr/bin/env python

import re

rgx = re.compile('^\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})\] (.*)$')
rgx_guardid = re.compile('Guard #(\d+) begins shift')

class Event(object):
  def __init__(self, s):
    (
      self.year,
      self.month,
      self.day,
      self.hour,
      self.min,
      self.eventtext
    ) = rgx.split(s)[1:-1]
    self.guardid = None
    self.type = None
    if self.eventtext.startswith('Guard'):
      self.guardid = rgx_guardid.split(self.eventtext)[1]
      self.type = 'BEGIN'
    elif self.eventtext == 'falls asleep':
      self.type = 'SLEEP'
    elif self.eventtext == 'wakes up':
      self.type = 'WAKE'

  def __repr__(self):
    return "[%s-%s-%s %s:%s] %s %s" % (self.year, self.month, self.day, self.hour, self.min, self.guardid, self.type)

class Guard(object):
  def __init__(self, guardid):
    self.guardid = guardid
    self.sleepmins = 0
    self.sleepmatrix = 60*[0]

events = []
with open('input.txt') as f:
  for line in f.readlines():
    events += [Event(line)]

events.sort(key=lambda e: (e.year, e.month, e.day, e.hour, e.min))

#print '\n'.join([str(e) for e in events])

for e in events:
  if e.guardid is not None:
    gid = e.guardid
  e.guardid = gid

print '\n'.join([str(e) for e in events])

guards = []
for e in events:
  if e.guardid not in [ g.guardid for g in guards]:
    guards += [Guard(e.guardid)]

for g in guards:
  guard_events = [ e for e in events if e.guardid == g.guardid ]
  t1 = None
  t2 = None
  for e in guard_events:
    if e.type == 'BEGIN':
      #print "BEGIN"
      t1 = None
      t2 = None
      continue
    elif e.type == 'SLEEP':
      t1 = int(e.min)
      #print "SLEEP %d" % t1
    elif e.type == 'WAKE':
      t2 = int(e.min)
      #print "WAKE %d" % t2
    if t1 is not None and t2 is not None:
      #print "CALCULATE"
      g.sleepmins += t2-t1
      for t in range(t1, t2):
        g.sleepmatrix[t] += 1
      t1 = None
      t2 = None
  print "Guard %5s slept %5d minutes total" % (g.guardid, g.sleepmins)

bestguard = sorted(guards, key=lambda g: g.sleepmins, reverse=True)[0]
print "Best guard seems to be %s with sleeptime %d" % (bestguard.guardid, bestguard.sleepmins)
print "The sleepmatrix is: %s" % bestguard.sleepmatrix
bestmin = bestguard.sleepmatrix.index(max(bestguard.sleepmatrix))
print "The best minute seems to be %d" % bestmin
print "Answer seems to be %d" % (int(bestguard.guardid) * bestmin)
