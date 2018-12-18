#!/usr/bin/env python

import sys
import time

recipescore = sys.argv[1]

def progress(s):
  sys.stdout.write("%s\r" % s)
  sys.stdout.flush()

recipes = "37"
elf1 = 0
elf2 = 1
scorelength = len(str(recipescore))
recipesontheleft = None
found = False
lastindex = 0
#print recipes
while not found:
  summa = int(recipes[elf1]) + int(recipes[elf2])
  newrecipes = ''.join([ str(d) for d in str(summa) ])
  recipes += newrecipes
  elf1 = (elf1 + 1 + int(recipes[elf1])) % len(recipes)
  elf2 = (elf2 + 1 + int(recipes[elf2])) % len(recipes)
  for i in xrange(lastindex, len(recipes)-scorelength):
    if recipes[i:i+scorelength] == recipescore:
      found = True
      recipesontheleft = i
      break
    lastindex += 1
  if len(recipes) % 1000000 == 0:
    progress("Number of recipes: %d" % len(recipes))
  #print recipes
  #time.sleep(1)

print "%s first appears after %d recipes" % (recipescore, recipesontheleft)
