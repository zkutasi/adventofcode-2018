#!/usr/bin/env python

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

R = [0]*4

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

samples_matched = []
for s in samples:
  num = 0
  for oname,oinstr in opcodes.items():
    Rbefore = list(s.before)
    Rafter = list(Rbefore)
    Rafter_expected = s.after
    Rafter[s.C] = oinstr(Rbefore, s.A, s.B)
    if Rafter == Rafter_expected:
      num += 1

  print "Sample %s matches %d opcode actions" % (s, num)
  samples_matched += [ ( num, s ) ]

print "The number of samples matching 3 or more opcodes: %d" % len(filter(lambda (num, sample): num>=3, samples_matched))
