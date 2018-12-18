#!/usr/bin/env python

num = 0
with open('input.txt') as f:
  for line in f.readlines():
    if line[0] == '+':
      num += int(line[1:])
    elif line[0] == '-':
      num -= int(line[1:])
    else:
      print "Hmmmm: %s" % line

print "FInal number is: %d" % num
