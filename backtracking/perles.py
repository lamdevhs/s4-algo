def validPartialNecklace(p, L):
  l = L[:p + 1]
  #print l, len(l)
  maxPatternLen = len(l) // 2
  #print "max", maxPatternLen, (len(l) // 2)
  for i in range(1, maxPatternLen + 1):
    left = l[-i:]
    right = l[-2*i:-i]
    #print "i"; i, left, right
    if left == right:
      return False
  return True


# L = [0,1,2,0,1,2,7]
# for i in range(7):
#   print L[:i + 1], validPartialNecklace(i, L)

def alwaysOk(p, L):
  return True

N = 15
L = range(N)



# ----------- callbacks
def saveRes(res, L):
  global cpt
  res.append(L[:])
  cpt += 1

class DummyBreak(Exception):
  pass

def breakOnFirst(res, L):
  print L
  raise DummyBreak()


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

def test(N, domain, validPartial, validSol, callback):
  global cpt, cptNode, cptNodeL
  cpt = 0
  cptNode = 0
  cptNodeL = (N + 1) * [0]
  res = []
  L = N * [0]
  try:
    backtrack(domain, validPartial, validSol, callback)(0,N,L,res)
  except DummyBreak:
    pass
  finally:
    print res
    print len(res), cpt, cptNode, cptNodeL

test(5, range(3), validPartialNecklace, alwaysOk, saveRes)