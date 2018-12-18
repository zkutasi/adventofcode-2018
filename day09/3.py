#!/usr/bin/env python

import re
import sys
from collections import deque

rgx = re.compile('(\d+) players; last marble is worth (\d+) points')

def progress(s):
  sys.stdout.write("%s\r" % s)
  sys.stdout.flush()

def game(player, lastmarble):
  circle = deque([0])
  marble = 1
  player = 0
  #print circle
  circle.append(1)
  marble += 1
  player += 1
  #print circle
  while marble <= lastmarble:
    if lastmarble/100 > 0 and marble % (lastmarble/100) == 0:
      progress("Placing marble %d/%d" % (marble, lastmarble))
    if marble%23 == 0:
      players[player] += marble
      circle.rotate(7)
      players[player] += circle.pop()
      circle.rotate(-1)
    else:
      circle.rotate(-1)
      circle.append(marble)
    marble += 1
    player = (player+1) % len(players)
    #print circle
    

with open('input.txt') as f:
  for line in f.readlines():
    players, lastmarble = rgx.split(line)[1:-1]
    players = [0]*int(players)
    game(players, int(lastmarble))
    print "Winner player's score: %d" % max(players)
    #break


