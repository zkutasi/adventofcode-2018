#!/usr/bin/env python

import re
import sys
import time
from collections import defaultdict
from collections import deque

class Instr(object):
  def __init__(self, instr):
    self.name = instr[0]
    self.A = int(instr[1])
    self.B = int(instr[2])
    self.C = int(instr[3])
  def __repr__(self):
    return "%4s %3d %3d %3d" % (self.name, self.A, self.B, self.C)

R = [0]*6
R[0] = 0

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
program_cache = defaultdict(lambda: False)
ipboundto = None
with open(sys.argv[1]) as f:
  for line in f.readlines():
    if line.startswith('#ip'):
      ipboundto = int(line.strip().split()[-1])
    else:
      instr += [ Instr(line.strip().split()) ]

print "Registers before execution: %s" % R

def print_state(ip_start, R_start, i, R):
  print "ip=%2d [%10s,%10s,%10s,%10s,%10s,%10s] %s [%10s,%10s,%10s,%10s,%10s,%10s]" % (
                             ip_start,
                             R_start[0],R_start[1],R_start[2],R_start[3],R_start[4],R_start[5],
                             i,
                             R[0],R[1],R[2],R[3],R[4],R[5]
        )

ip = 0
loop_to_check_list = deque([ ])

loop_to_check_list.append( ( 18,
                             (0, 0, 0, 0, -1, 0),
                             ("R[4] = R[1]/256",)
                           )
                         )


seen_r3s = set()
if len(loop_to_check_list) > 0:
  ltc = loop_to_check_list.popleft()
else:
  ltc = None
while ip >= 0 and ip < len(instr):
  ip_start = ip
  R_start = list(R)
  i = instr[ip]
  if ltc is not None:
    program_cache[ (ip_start, R_start[0],R_start[1],R_start[2],R_start[3],R_start[4],R_start[5]) ] = True
    is_cached = program_cache[ (ltc[0], R_start[0]+ltc[1][0],
                                        R_start[1]+ltc[1][1],
                                        R_start[2]+ltc[1][2],
                                        R_start[3]+ltc[1][3],
                                        R_start[4]+ltc[1][4],
                                        R_start[5]+ltc[1][5]) ]
    if is_cached:
      #print "Found loop, modifying Registers"
      for r in ltc[2]:
        exec(r)
      R_start = list(R)
      #print_state(ip_start, R_start, i, R)
      program_cache.clear()
  R[ipboundto] = ip
  R[i.C] = opcodes[i.name](R, i.A, i.B)
  ip = R[ipboundto]
  ip += 1

  if ip_start == 28 and R[1] < 256:
    print_state(ip_start, R_start, i, R)
    if R[3] not in seen_r3s:
      seen_r3s.add(R[3])
    else:
      print "Found loop in R[3] values"
      break
  #print_state(ip_start, R_start, i, R)
  #time.sleep(0.1)
  

print "Registers after execution: %s" % R
