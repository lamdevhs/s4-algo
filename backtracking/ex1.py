def validSol(p, L):
  [i, j, k, l] = L[0:N]
  return (
    i != j 
    and k != l
    and i + k < j)

D = range(4)
invalid = -1
N = 4
L = N * [invalid] # range(N)

def alwaysOk(p, L):
  return True

def validPartial(p, L):
  [i, j, k, l] = L[0:N]
  if p == 0:
    return True
  if p == 1:
    return i != j
  if p == 2:
    return i + k < j
  if p == 3:
    return k != l
  else:
    raise Exception("invalid `p`")



#-----------------

def iter():
  sol = []
  for i in D:
    for j in D:
      for k in D:
        for l in D:
          L = [i, j, k, l]
          if validSol(0, L):
            sol.append(L)
  return sol


print iter()
print len(iter())

print;print;print




def saveRes(res, L):
  global cpt
  res.append(L[:])
  cpt += 1

def breakOnFirst(res, L):
  print L
  raise Exception()

cpt = 0
cptNode = 0
cptNodeL = (N + 1) * [0]

def backtrack(validPartial, validSol, callback):
  def f(p, N, L, res):
    global cptNode
    cptNode += 1
    cptNodeL[p] += 1
    if p >= N:
      if validSol(p, L):
        callback(res, L)
    else:
      for v in D:
        L[p] = v
        if validPartial(p, L):
          f(p + 1, N, L, res)
      # L[p] = invalid
  return f


def test(validPartial, validSol, callback):
  global cpt, cptNode, cptNodeL
  cpt = 0
  cptNode = 0
  cptNodeL = (N + 1) * [0]
  res = []
  try:
    backtrack(validPartial, validSol, callback)(0,N,L,res)
  except:
    pass
  finally:
    print len(res), cpt, cptNode, cptNodeL

test(alwaysOk, validSol, saveRes)
test(validPartial, alwaysOk, saveRes)
# res2 = []
# cpt = 0
# cptNode = 0
# cptNodeL = (N + 1) * [0]
# backtrack(validPartial, alwaysOk, saveRes)(0,N,L, res2)
# print len(res2), cpt, cptNode, cptNodeL


test(validPartial, alwaysOk, breakOnFirst)
# try:
#   res3 = None
#   cpt = 0
#   cptNode = 0
#   cptNodeL = (N + 1) * [0]
#   backtrack(validPartial, alwaysOk, breakOnFirst)(0,N,L,res3)
  
# except:
#   print cpt, cptNode, cptNodeL
