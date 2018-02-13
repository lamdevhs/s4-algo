import time

prix = [20,18,8]
poids = [4,3,2]

def sol(n):
  L = [0,0,8,18,20]
  for i in range(5,n + 1):
    resL = []
    for k in range(len(prix)):
      resL.append(prix[k] + L[i - poids[k]])
    L.append(max(resL))
  return L[n]



def exhaust(n):
  res = 0
  i = 0
  j = 0
  k = 0
  while True:
    if i*3 > n:
          break
    j = 0
    while True:
      if i*3 + j*4 > n:
          break
      k = 0
      while True:
        if i*3 + j*4 + k*2 > n:
          break
        resHere = i*18 + j*20 + k*8
        res = max(resHere, res)
        k += 1
      j += 1
    i += 1
  return res



def glutton(n):
  L = [0,0,8,18,20]
  if n <= 4:
    return L[n]

  for k in range(len(prix)):
    if n - poids[k] >= 0:
      return prix[k] + glutton(n - poids[k])

print glutton(10)
print glutton(1000)

def comparer(fs, n):
  print "n =", n
  for f in fs:
    s = time.clock()
    res = f(n)
    t = time.clock() - s
    print "  ", f.func_name, ":", res, t

fs = [sol, exhaust, glutton]

for i in range(1,4):
  comparer(fs, 10**i)
