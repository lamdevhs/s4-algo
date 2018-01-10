from collections import Counter


pieces931 = [9,3,1] # sorted
pieces431 = [4,3,1] # sorted

def glutton1(pieces, N):
  assert(isSortedDesc(pieces))
  ps = pieces[:]
  res = []
  while len(ps) != 0:
    if ps[0] <= N:
      N -= ps[0]
      res.append(ps[0])
    else:
      ps.pop(0)
  if N != 0:
    return -1
  else:
    return res
    #return len(res)

def glutton1_rec(pieces, N, res, firstLoop = True):
  if firstLoop:
    assert(isSortedDesc(pieces))
  if pieces == []:
    if N != 0:
      return -1
    else:
      return len(res)
  else:
    if pieces[0] <= N:
      N -= pieces[0]
      res.append(pieces[0])
      allowedNow = pieces
    else:
      allowedNow = pieces[:]
      allowedNow.pop(0)
    return glutton1_rec(allowedNow, N, res, False)
  
def isSortedDesc(xs):
  for i in range(len(xs) - 1):
    if xs[i] < xs[i + 1]:
      return False
  return True
    
print glutton1(pieces931, 10)
print glutton1_rec(pieces931, 10, [])

def combinaisons(pieces, nb):
  if nb == 0:
    return []

  res = map(lambda v: [v], pieces)
  while len(res[0]) != nb:
    newRes = []
    for l in res:
      last = l[-1]
      infEq = filter(lambda v: v <= last, pieces)
      ls = prod(l, infEq)
      newRes += ls
    res = newRes
  return res

def prod (l, pieces):
  res = []
  for v in pieces:
    res.append(l + [v])
  return res

def sommesPossibles(pieces, nb):
  cs = combinaisons(pieces, nb)
  return map(lambda l: sum(l), cs)
    
def sommesDoubles(pieces, nb):
  sommes = sommesPossibles(pieces, nb)
  c = Counter(sommes)
  res = []
  for k in c:
    if c[k] >= 2:
      res.append(k)
  return res
  
print sommesDoubles(pieces431, 4)

  
  

