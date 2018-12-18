#!/usr/bin/env python

import re
import sys

rgx = re.compile('(\d+) players; last marble is worth (\d+) points')

def progress(s):
  sys.stdout.write("%s\r" % s)
  sys.stdout.flush()

class Node(object):
  def __init__(self, value, prv=None, nxt=None):
    self.value = value
    self.prv = prv
    self.nxt = nxt
  def print_circle(self):
    lst = [self.value]
    curr = self
    while curr.nxt is not None and curr.nxt.value != self.value:
      lst += [curr.nxt.value]
      curr = curr.nxt
    print lst

def playgame(player, lastmarble):
  marble = 0
  curr = Node(marble)
  first = curr
  marble += 1
  #first.print_circle()
  player = 0
  newnode = Node(marble, curr, curr)
  curr.nxt = newnode
  curr.prv = newnode
  curr = newnode
  marble += 1
  player += 1
  #first.print_circle()
  while marble <= lastmarble:
    if lastmarble/100 > 0 and marble % (lastmarble/100) == 0:
      progress("Placing marble %d/%d" % (marble, lastmarble))
    if marble%23 == 0:
      players[player] += marble
      back7th = curr.prv.prv.prv.prv.prv.prv.prv
      curr = back7th.nxt
      back7th.prv.nxt = back7th.nxt
      back7th.nxt.prv = back7th.prv
      players[player] += back7th.value
    else:
      n1 = curr.nxt
      n2 = curr.nxt.nxt
      newnode = Node(marble, n1, n2)
      n1.nxt = newnode
      n2.prv = newnode
      curr = newnode
    marble += 1
    player = (player+1) % len(players)
    #first.print_circle()
    

games = []
with open('input.txt') as f:
  for line in f.readlines():
    players, lastmarble = rgx.split(line)[1:-1]
    games += [ (players, lastmarble) ]

for game in games:
  players, lastmarble = game
  players = [0]*int(players)
  playgame(players, int(lastmarble))
  print "Winner player's score: %d" % max(players)
  #break
