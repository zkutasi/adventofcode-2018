#!/usr/bin/env python

import sys

recipenum = int(sys.argv[1])

recipes = [3, 7]
elf1 = 0
elf2 = 1
scorelength = 10
#print recipes
while len(recipes) < recipenum + scorelength:
  summa = recipes[elf1] + recipes[elf2]
  newrecipes = [ int(d) for d in str(summa) ]
  recipes += newrecipes
  elf1 = (elf1 + 1 + recipes[elf1]) % len(recipes)
  elf2 = (elf2 + 1 + recipes[elf2]) % len(recipes)
  #print recipes

print "Recipe score after %d recipes: %s" % (recipenum, recipes[recipenum:recipenum + scorelength])
