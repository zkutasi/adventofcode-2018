#!/usr/bin/env python

import sys
import re
import time

rgx = re.compile('(\d+) units each with (\d+) hit points(.*)with an attack that does (\d+) (\S+) damage at initiative (\d+)')

class Group(object):
  def __init__(self, troopsfor, groupid, units, hitpoints, damage, damagetype, initiative, immuneto, weakto):
    self.troopsfor = troopsfor
    self.groupid = groupid
    self.units = units
    self.hitpoints = hitpoints
    self.damage = damage
    self.damagetype = damagetype
    self.initiative = initiative
    self.immuneto = immuneto
    self.weakto = weakto
    self.effectivepower = self.units * self.damage
    self.chosentarget = None
    self.dead = False
  def __repr__(self):
    immunetostr = "immune to %s" % ', '.join(self.immuneto)
    weaktostr = "weak to %s" % ', '.join(self.weakto)
    extrastr = "" if len(self.immuneto) + len(self.weakto) == 0 else "(%s) " % (
      ("%s; %s" % (immunetostr, weaktostr)) if len(self.immuneto) > 0 and len(self.weakto) > 0 else
      ("%s" % (immunetostr if len(self.immuneto) > 0 else weaktostr) )
    )
    return "%d units each with %d hit points %swith an attack that does %d %s damage at initiative %d" % (
      self.units, self.hitpoints, extrastr, self.damage, self.damagetype, self.initiative
    )
  def __str__(self):
    return self.__repr__()
  def get_damage_amount_to_enemy(self, enemy, printout=True):
    damage = self.effectivepower
    if self.damagetype in enemy.immuneto:
      damage = 0
    if self.damagetype in enemy.weakto:
      damage *= 2
    if printout and not self.dead:
      print "%s group %d would deal defending group %d %d damage" % (
            "Immune System" if self.troopsfor == 'IS' else "Infection",
            self.groupid,
            enemy.groupid,
            damage
      )
    return damage
  def take_damage(self, damage):
    unitskilled = min(damage / self.hitpoints, self.units)
    self.units -= unitskilled
    self.effectivepower = self.units * self.damage
    if self.units <= 0:
      self.dead = True
    return unitskilled

groups = []
with open(sys.argv[1]) as f:
  troopsfor = None
  for line in f.readlines():
    if len(line.strip()) == 0:
      pass
    elif line.startswith('Immune System'):
      troopsfor = 'IS'
      groupid = 1
    elif line.startswith('Infection'):
      troopsfor = 'I'
      groupid = 1
    else:
      units, hitpoints, extra, damage, damagetype, initiative = rgx.split(line)[1:-1]
      units = int(units)
      hitpoints = int(hitpoints)
      damage = int(damage)
      initiative = int(initiative)
      extras = extra.split(';')
      immuneto = []
      weakto = []
      for e in [ e.strip().replace('(','').replace(')','') for e in extras ]:
        if e.startswith('immune to'):
          immuneto = e.replace('immune to ', '').split(', ')
        elif e.startswith('weak to'):
          weakto = e.replace('weak to ', '').split(', ')

      g = Group(troopsfor, groupid, units, hitpoints, damage, damagetype, initiative, immuneto, weakto)
      groups += [ g ]
      groupid += 1

def print_state():
  print "Immune System:"
  remaining_groups = [ g for g in groups if g.troopsfor == 'IS' and not g.dead ]
  if len(remaining_groups) == 0:
    print "No groups remain"
  else:
    for g in remaining_groups:
      print "Group %d contains %d units" % (g.groupid, g.units)
  print "Infection:"
  remaining_groups = [ g for g in groups if g.troopsfor == 'I' and not g.dead ]
  if len(remaining_groups) == 0:
    print "No groups remain"
  else:
    for g in remaining_groups:
      print "Group %d contains %d units" % (g.groupid, g.units)
  print

def target_selection():
  for g in groups:
    g.chosentarget = None

  print_state()

  for g in sorted(groups, key=lambda g: (-g.effectivepower, -initiative) ):
    chosentarget = None
    enemies = sorted([ e for e in groups if e.troopsfor != g.troopsfor and
                                            not e.dead and
                                            g.get_damage_amount_to_enemy(e) > 0 and
                                            e not in set([ gr.chosentarget for gr in groups if gr.chosentarget is not None ]) ],
                     key=lambda e: (-g.get_damage_amount_to_enemy(e), -e.effectivepower, -e.initiative))
    if len(enemies) > 0:
      chosentarget = enemies[0]
    g.chosentarget = chosentarget
  print

def attacking():
  for g in sorted(groups, key=lambda g: -g.initiative):
    if g.chosentarget is not None and not g.dead:
      enemy = g.chosentarget
      damage = g.get_damage_amount_to_enemy(enemy, printout=False)
      unitskilled = enemy.take_damage(damage)
      print "%s group %d attacks defending group %d, killing %d units" % (
            "Immune System" if g.troopsfor == 'IS' else "Infection",
            g.groupid,
            enemy.groupid,
            unitskilled
      )


print "Immune System:"
print '\n'.join([ str(g) for g in groups if g.troopsfor == 'IS' ])
print
print "Infection:"
print '\n'.join([ str(g) for g in groups if g.troopsfor == 'I' ])
print


r = 1
while len([ g for g in groups if g.troopsfor == 'IS' and not g.dead ]) > 0 and \
      len([ g for g in groups if g.troopsfor == 'I' and not g.dead ]) > 0:
  print
  print "Round %3d:" % r
  print "=========="
  target_selection()
  attacking()
  r += 1
  print


print_state()
print "Winning army has %d units" % sum([ g.units for g in groups if not g.dead ])
