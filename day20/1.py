#!/usr/bin/env python

import sys

def pass_rooms(routes):
  def inner(route_idx):
    rooms_passed_options = [0]
    while routes[route_idx] not in (')', '$'):
      print "Handling char %s" % routes[route_idx]
      if routes[route_idx] in ('('):
        route_idx, rp = inner(route_idx+1)
        rooms_passed_options[-1] += rp
      elif routes[route_idx] in ('|'):
        rooms_passed_options.append(0)
      else:
        rooms_passed_options[-1] += 1

      print "State so far is %s" % rooms_passed_options
      route_idx += 1

    return (route_idx, max(rooms_passed_options))

  return inner(1)[1]

with open(sys.argv[1]) as f:
  for line in f.readlines():
    routes = line.strip()
    changed = True
    while changed:
      changed = False
      l1 = len(routes)
      routes = routes.replace('WE', '').replace('EW', '')
      routes = routes.replace('NS', '').replace('SN', '')
      l2 = len(routes)
      if l2 < l1:
        changed = True
    print pass_rooms(routes)

