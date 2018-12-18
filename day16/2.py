#!/usr/bin/env python

from collections import defaultdict
import re
import sys

rgx = re.compile('(Before|After):\s+\[(.*)\]')

class Instr(object):
  def __init__(self, before, instr, after):
    self.before = before
    self.instr = instr
    self.n = instr[0]
    self.A = instr[1]
    self.B = instr[2]
    self.C = instr[3]
    self.after = after
  def __repr__(self):
    return "Before: %s, %s, After: %s" % (str(self.before), str(self.instr), str(self.after))

opcodes = {
            'addr': lambda R,A,B: R[A] + R[B],
            'addi': lambda R,A,B: R[A] + B,
            'mulr': lambda R,A,B: R[A] * R[B],
            'muli': lambda R,A,B: R[A] * B,
            'banr': lambda R,A,B: R[A] & R[B],
            'bani': lambda R,A,B: R[A] & B,
            'borr': lambda R,A,B: R[A] | R[B],
            'bori': lambda R,A,B: R[A] | B,
            'setr': lambda R,A,B: R[A],
            'seti': lambda R,A,B: A,
            'gtir': lambda R,A,B: 1 if A > R[B] else 0,
            'gtri': lambda R,A,B: 1 if R[A] > B else 0,
            'gtrr': lambda R,A,B: 1 if R[A] > R[B] else 0,
            'eqir': lambda R,A,B: 1 if A == R[B] else 0,
            'eqri': lambda R,A,B: 1 if R[A] == B else 0,
            'eqrr': lambda R,A,B: 1 if R[A] == R[B] else 0
          }

puzzle1 = False
samples = []
instructions = []
with open(sys.argv[1]) as f:
  before = None
  instr = None
  after = None
  for line in f.readlines():
    if len(line.strip()) == 0:
      continue
    if line.startswith('Before'):
      before = [ int(e.strip()) for e in rgx.split(line)[2].split(',') ]
      puzzle1 = True
    elif line.startswith('After'):
      after = [ int(e.strip()) for e in rgx.split(line)[2].split(',') ]
      samples += [ Instr(before, instr, after) ]
      puzzle1 = False
    else:
      instr = [ int(e.strip()) for e in line.split() ]
      if not puzzle1:
        instructions += [ instr ]

def printout_candidates():
  print '\n'.join(sorted([ "%2d=%s" % (opcodenum, str(candidates)) for opcodenum,candidates in sorted(samples_matched.items(), key=lambda (k,v): k) ]))

samples_matched = defaultdict(lambda: set(opcodes.keys()))
for s in samples:
  opcodelist = set([])
  for oname,oinstr in opcodes.items():
    Rbefore = list(s.before)
    Rafter = list(Rbefore)
    Rafter_expected = s.after
    Rafter[s.C] = oinstr(Rbefore, s.A, s.B)
    if Rafter == Rafter_expected:
      opcodelist.add(oname)

  #print "Sample %s matches opcode %s" % (s, str(opcodelist))
  samples_matched[s.instr[0]] = samples_matched[s.instr[0]] & opcodelist

print "Candidates at the beginning:"
printout_candidates()

somethingdone = True
while somethingdone and len([ opcodenum for opcodenum,candidates in samples_matched.items() if len(candidates) > 1 ]) > 0:
  somethingdone = False
  found_opcodes = [ next(iter(candidates)) for opcodenum,candidates in samples_matched.items() if len(candidates) == 1 ]
  for foundc in found_opcodes:
    opcodes2process = [ (opcodenum,candidates) for opcodenum,candidates in samples_matched.items() if len(candidates) > 1 ]
    for o,c in opcodes2process:
      if foundc in c:
        somethingdone = True
        samples_matched[o].remove(foundc)

for opcodenum,candidates in samples_matched.items():
  samples_matched[opcodenum] = samples_matched[opcodenum].pop()
print "Candidates resolved:"
printout_candidates()

R = [0]*4
print "R=%s" % R
for i in instructions:
  opcode = opcodes[ samples_matched[ i[0] ] ]
  R[i[3]] = opcode(R, i[1], i[2])
  #print "R=%s" % R

print "R=%s" % R
