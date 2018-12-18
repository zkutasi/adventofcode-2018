#!/usr/bin/env python

import sys

def loopfreq(freq, freqs):
  found = False
  with open(sys.argv[1]) as f:
    for line in f.readlines():
      if line[0] == '+':
        freq += int(line[1:])
      elif line[0] == '-':
        freq -= int(line[1:])
      else:
        print "Hmmmm: %s" % line
      if freq in freqs:
        print "First repetition found: %s" % freq
        found=True
        break
      freqs.add(freq)

  if not found:
    loopfreq(freq, freqs)

loopfreq(0, set([0]))
