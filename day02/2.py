#!/usr/bin/env python

with open('input.txt') as f:
  ids = f.read().splitlines()
  for idx1, id1 in enumerate(ids):
    for idx2, id2 in enumerate(ids):
      if idx2 <= idx1:
        continue
      differ = 0
      for c1, c2 in zip(id1, id2):
        if c1 != c2:
          differ += 1
      if differ == 1:
        print "Possibly:"
        print id1
        print id2
    
