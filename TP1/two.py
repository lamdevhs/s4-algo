def guardsLocation(paintings, guardSight):
  halfSight = guardSight / 2.
  rest = paintings[:]
  rest.sort()
  last = rest[-1]
  first = rest[0]
  distance = last - first
  if distance == 0:
    return [first]

  guards = []
  while distance > 0:
    guards.append(rest[0] + halfSight)
    distance -= guardSight
    rightMax = rest[0] + guardSight
    rest = filter(lambda v: v > rightMax, rest)
  return guards

def remainingPaintings(ps, min):
  res = []
  for p in ps:
    if p > min:
      res.append(p)
  return res

print guardsLocation([1,2,4,5.2,8.4], 4)
