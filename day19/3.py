#!/usr/bin/env python

import re
import sys
import time
from collections import defaultdict
from collections import deque
from math import sqrt, floor

class Instr(object):
  def __init__(self, instr):
    self.name = instr[0]
    self.A = int(instr[1])
    self.B = int(instr[2])
    self.C = int(instr[3])
  def __repr__(self):
    return "%4s %2d %2d %2d" % (self.name, self.A, self.B, self.C)

R = [0]*6
R[0] = 1

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

def get_divisors(n):
  divs = deque([])
  for d in range(int(floor(sqrt(n))), 0, -1):
    if n % d ==0:
      divs.appendleft(d)
      divs.append(n/d)
  return divs



loop_to_check_list = deque([])
def prepare_loopdetector(bignumber):
  divisors = get_divisors(bignumber)
  print "Divisors of %d are %s" % (bignumber, divisors)
  for d in divisors:
    loop_to_check_list.append( ( 3,
                                 (0, 0, -1, 0, 0, 0),
                                 ((2, bignumber/d), (4, d)))
                             )
  loop_to_check_list.append( ( 3,
                               (0, 0, -1, 0, 0, 0),
                               ((2, bignumber),))
                           )
  

ip = 0
bignumber = None
ltc = None
while ip >= 0 and ip < len(instr):
  ip_start = ip
  R_start = list(R)
  i = instr[ip]
  if bignumber is not None and ltc is not None:
    program_cache[ (ip_start, R_start[0],R_start[1],R_start[2],R_start[3],R_start[4],R_start[5]) ] = True
    is_cached = program_cache[ (ltc[0], R_start[0]+ltc[1][0],
                                        R_start[1]+ltc[1][1],
                                        R_start[2]+ltc[1][2],
                                        R_start[3]+ltc[1][3],
                                        R_start[4]+ltc[1][4],
                                        R_start[5]+ltc[1][5]) ]
    if is_cached:
      print "Found loop, modifying Registers"
      for r1, r2 in ltc[2]:
        R[r1] = r2
      R_start = list(R)
      print_state(ip_start, R_start, i, R)
      if len(loop_to_check_list) > 0:
        program_cache.clear()
        ltc = loop_to_check_list.popleft()
      else:
        ltc = None
  R[ipboundto] = ip
  R[i.C] = opcodes[i.name](R, i.A, i.B)
  ip = R[ipboundto]
  ip += 1
  if ip == 1:
    bignumber = R[5]
    prepare_loopdetector(bignumber)
    ltc = loop_to_check_list.popleft()

  if R[0] != R_start[0]:
    print "R[0] changed: "
    print_state(ip_start, R_start, i, R)
    time.sleep(0.02)
  else:
    print_state(ip_start, R_start, i, R)
    time.sleep(0.02)
  

print "Registers after execution: %s" % R
