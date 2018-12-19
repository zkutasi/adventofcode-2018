#!/usr/bin/env python

import re
import sys

class Instr(object):
  def __init__(self, instr):
    self.name = instr[0]
    self.A = int(instr[1])
    self.B = int(instr[2])
    self.C = int(instr[3])
  def __repr__(self):
    return "%s %d %d %d" % (self.name, self.A, self.B, self.C)

R = [0]*6

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

instr = []
ipboundto = None
with open(sys.argv[1]) as f:
  for line in f.readlines():
    if line.startswith('#ip'):
      ipboundto = int(line.strip().split()[-1])
    else:
      instr += [ Instr(line.strip().split()) ]

print "Registers before execution: %s" % R

ip = 0
while ip >= 0 and ip < len(instr):
  ip_start = ip
  R_start = list(R)
  i = instr[ip]
  R[ipboundto] = ip
  R[i.C] = opcodes[i.name](R, i.A, i.B)
  ip = R[ipboundto]
  ip += 1
  #print "ip=%d %s %s %s" % (ip_start, R_start, i, R)
  

print "Registers after execution: %s" % R
