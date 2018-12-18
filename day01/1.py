#!/usr/bin/env python

import sys

num = 0
with open(sys.argv[1]) as f:
  for line in f.readlines():
    if line[0] == '+':
      num += int(line[1:])
    elif line[0] == '-':
      num -= int(line[1:])
    else:
      print "Hmmmm: %s" % line

print "FInal number is: %d" % num
