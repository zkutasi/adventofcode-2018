#!/usr/bin/env python

import copy
import time
import sys

decisions = [ 'L', 'T', 'R' ]

class Cart(object):
  def __init__(self, locx, locy, rep):
    self.locx = locx
    self.locy = locy
    self.rep = rep
    self.decision = 0
    self.hasmoved = False
  def move(self):
    self.hasmoved = True
    if self.rep == '>':
      self.locx += 1
      if tracks[self.locy][self.locx] == '/':
        self.rep = '^'
      elif tracks[self.locy][self.locx] == '\\':
        self.rep = 'v'
      elif tracks[self.locy][self.locx] == '+':
        if decisions[self.decision] == 'L':
          self.rep = '^'
        elif decisions[self.decision] == 'T':
          pass
        elif decisions[self.decision] == 'R':
          self.rep = 'v'
        self.decision = (self.decision + 1) % 3
    elif self.rep == '<':
      self.locx -= 1
      if tracks[self.locy][self.locx] == '/':
        self.rep = 'v'
      elif tracks[self.locy][self.locx] == '\\':
        self.rep = '^'
      elif tracks[self.locy][self.locx] == '+':
        if decisions[self.decision] == 'L':
          self.rep = 'v'
        elif decisions[self.decision] == 'T':
          pass
        elif decisions[self.decision] == 'R':
          self.rep = '^'
        self.decision = (self.decision + 1) % 3
    elif self.rep == '^':
      self.locy -= 1
      if tracks[self.locy][self.locx] == '/':
        self.rep = '>'
      elif tracks[self.locy][self.locx] == '\\':
        self.rep = '<'
      elif tracks[self.locy][self.locx] == '+':
        if decisions[self.decision] == 'L':
          self.rep = '<'
        elif decisions[self.decision] == 'T':
          pass
        elif decisions[self.decision] == 'R':
          self.rep = '>'
        self.decision = (self.decision + 1) % 3
    elif self.rep == 'v':
      self.locy += 1
      if tracks[self.locy][self.locx] == '/':
        self.rep = '<'
      elif tracks[self.locy][self.locx] == '\\':
        self.rep = '>'
      elif tracks[self.locy][self.locx] == '+':
        if decisions[self.decision] == 'L':
          self.rep = '>'
        elif decisions[self.decision] == 'T':
          pass
        elif decisions[self.decision] == 'R':
          self.rep = '<'
        self.decision = (self.decision + 1) % 3


def print_tracks():
  tracks_with_carts = copy.deepcopy(tracks)
  for cart in carts:
    tracks_with_carts[cart.locy][cart.locx] = cart.rep
  for line in tracks_with_carts:
    print ''.join(line)

tracks = []
with open(sys.argv[1]) as f:
  for line in f.readlines():
    tracks += [ [ c for c in line.replace('\n', '') ] ]

print "Track of %sx%s loaded..." % (len(tracks), len(tracks[0]))

carts = []
for j in xrange(len(tracks)):
  for i in xrange(len(tracks[0])):
    if tracks[j][i] in ('v', '^', '<', '>'):
      c = Cart(i, j, tracks[j][i])
      carts += [ c ]
      if c.rep in ('v', '^'):
        tracks[j][i] = '|'
      else:
        tracks[j][i] = '-'

print "Carts extracted..."

#print_tracks()
crash = False
while not crash:
  #print_tracks()
  carts_tomove = sorted(filter(lambda c: not c.hasmoved, carts), key=lambda c: (c.locy, c.locx))
  if len(carts_tomove) > 0:
    carts_tomove[0].move()
  else:
    for cart in carts:
      cart.hasmoved = False
    continue

  for cart in carts:
    if len(filter(lambda c: c.locx == cart.locx and c.locy == cart.locy, carts)) > 1:
      print "CRASH at (%s, %s) !!!" % (cart.locx, cart.locy)
      sys.exit(0)
