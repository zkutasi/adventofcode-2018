#!/usr/bin/env python

import sys

def mapper(id):
  m = {}
  for c in id:
    if c in m.keys():
      m[c] += 1
    else:
      m[c] = 1
  return m

with open(sys.argv[1]) as f:
  doubles=0
  tripples=0
  for line in f.readlines():
    m = mapper(line)
    if 2 in m.values():
      doubles += 1
    if 3 in m.values():
      tripples += 1

print "Checksum: %s" % (doubles*tripples,)
