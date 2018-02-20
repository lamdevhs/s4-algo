def validSol(S):
  def f(p, L):
    return (sum(L) == S
      and sorted(list(set(L))) == L)
  return f

invalid = -1
N = 5
L = N * [invalid] # range(N)

def alwaysOk(p, L):
  return True

def validPartial(S):
  def f (p, L):
    if p == 0:
      return  L[p] <= S
    elif p == len(L) - 1:
      return (L[p] > L[p - 1] and sum(L[:p+1]) == S)
    else:
      return (L[p] > L[p - 1] and sum(L[:p+1]) <= S)
  return f

def saveRes(res, L):
  global cpt
  res.append(L[:])
  cpt += 1
  print L

class DummyBreak(Exception):
  pass

def breakOnFirst(res, L):
  print L
  raise DummyBreak()

#-----------------

def iter(S):
  sol = []
  for i in range(1, S):
    for j in range(i + 1, S - i + 1):
      for k in range(j + 1, S - i - j + 1):
        for l in range(k + 1, S - i - j - k + 1):
          for m in range(l + 1, S - i - j - k - l + 1):
            L = [i, j, k, l, m]
            #print sum(L)
            if validSol(S)(0, L):
              sol.append(L)
  return sol


print iter(18); print len(iter(18))

print;print;print


def backtrack(domain, validPartial, validSol, callback):
  def f(p, N, L, res):
    global cptNode
    cptNode += 1
    cptNodeL[p] += 1
    if p >= N:
      if validSol(p, L):
        callback(res, L)
    else:
      for v in domain:
        L[p] = v
        if validPartial(p, L):
          f(p + 1, N, L, res)
      # L[p] = invalid
  return f


def test(domain, validPartial, validSol, callback):
  global cpt, cptNode, cptNodeL
  cpt = 0
  cptNode = 0
  cptNodeL = (N + 1) * [0]
  res = []
  try:
    backtrack(domain, validPartial, validSol, callback)(0,N,L,res)
  except DummyBreak:
    pass
  finally:
    print len(res), cpt, cptNode, cptNodeL

S = 18
test(range(1,S), alwaysOk, validSol(S), saveRes)
test(range(1,S), validPartial(S), alwaysOk, saveRes)
