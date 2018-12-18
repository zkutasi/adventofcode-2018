#!/usr/bin/env python

import re

rgx = re.compile('Step (.) must be finished before step (.) can begin.')

class Step(object):
  def __init__(self, name):
    self.name = name
    self.isready = False
    self.dependson = []
    self.exectime = 0-ord(name)+64
  def __repr__(self):
    return self.name

class Worker(object):
  def __init__(self, id):
    self.id = id
    self.workingon = None
  def __repr__(self):
    return '.' if self.workingon is None else self.workingon.name

steps = {}
with open('input.txt') as f:
  for line in f.readlines():
    a,b = rgx.split(line)[1:-1]
    if a not in steps:
      steps[a] = Step(a)
    if b not in steps:
      steps[b] = Step(b)
    steps[b].dependson += [ steps[a] ]

steps = sorted(steps.values(), key=lambda s: s.name)

workers = []
for w in range(5):
  workers += [Worker(w)]

time = 0
donesteps = ''
print "%6s %8s %8s %8s %8s %8s %s" % ('Second', 'Worker1', 'Worker2', 'Worker3', 'Worker4', 'Worker5', 'Done')
while not all([ s.isready for s in steps ]):
  freeworkers = [ w for w in workers if w.workingon is None ]
  for fw in freeworkers:
    work_available = [ s for s in steps
                       if not s.isready and
                         all([ dep.isready for dep in s.dependson ]) and
                         s not in [ w.workingon
                                    for w in workers
                                    if w.workingon is not None
                                  ]
                     ]
    if len(work_available) > 0:
      work = work_available.pop(0)
      fw.workingon = work
  print "%6s %8s %8s %8s %8s %8s %s" % (time, workers[0], workers[1], workers[2], workers[3], workers[4], donesteps)
  for w in workers:
    if w.workingon is not None:
      w.workingon.exectime += 1
      if w.workingon.exectime == 60:
        w.workingon.isready = True
        donesteps += w.workingon.name
        #print "Step %s is ready" % w.workingon.name
        w.workingon = None
  time += 1

print "Total time spent: %d" % time
