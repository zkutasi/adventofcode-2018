#!/usr/bin/env python

import re
import sys

rgx = re.compile('(\d+) players; last marble is worth (\d+) points')

def progress(s):
  sys.stdout.write("%s\r" % s)
  sys.stdout.flush()

def get_new_index(lencircle, curr):
  newindex = curr + 2
  if newindex > lencircle:
    newindex = newindex-lencircle
  return newindex

def get_7th_back(lencircle, curr):
  newindex = curr - 7
  if newindex < 0:
    newindex = newindex+lencircle
  return newindex

def game(player, lastmarble):
  circle = [0]
  curr = 0
  marble = 1
  player = 0
  #print circle
  circle.insert(1, 1)
  curr += 1
  marble += 1
  player += 1
  #print circle
  while marble <= lastmarble:
    if lastmarble/100 > 0 and marble % (lastmarble/100) == 0:
      progress("Placing marble %d/%d" % (marble, lastmarble))
    if marble%23 == 0:
      players[player] += marble
      pop7 = get_7th_back(len(circle), curr)
      newindex = pop7
      players[player] += circle.pop(pop7)
    else:
      newindex = get_new_index(len(circle), curr)
      circle.insert(newindex, marble)
    marble += 1
    curr = newindex
    player = (player+1) % len(players)
    #print circle
    

with open('input.txt') as f:
  for line in f.readlines():
    players, lastmarble = rgx.split(line)[1:-1]
    players = [0]*int(players)
    game(players, int(lastmarble))
    print "Winner player's score: %d" % max(players)
    #break


