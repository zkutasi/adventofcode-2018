#!/usr/bin/env python

import re
import sys

rgx = re.compile('Step (.) must be finished before step (.) can begin.')

class Step(object):
  def __init__(self, name):
    self.name = name
    self.isready = False
    self.dependson = []


steps = {}
with open(sys.argv[1]) as f:
  for line in f.readlines():
    a,b = rgx.split(line)[1:-1]
    if a not in steps:
      steps[a] = Step(a)
    if b not in steps:
      steps[b] = Step(b)
    steps[b].dependson += [ steps[a] ]

steps = sorted(steps.values(), key=lambda s: s.name)
orderofsteps = ""

while not all([s.isready for s in steps]):
  for idx, step in enumerate(steps):
    if not step.isready and all([s.isready for s in step.dependson]):
      orderofsteps += step.name
      step.isready = True
      break

print "Order of steps: %s" % orderofsteps
