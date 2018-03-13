import time
#-----------------

def checkLine(L, p, N):
  line = p // N
  col = p % N
  v = L[p]
  for i in range(col):
    ix = line*N + i
    x = L[ix]
    if x == v:
      return False
  return True

def checkColumn(L, p, N):
  col = p % N
  line = p // N
  v = L[p]
  for i in range(line):
    ix = col + i*N
    x = L[ix]
    if x == v:
      return False
  return True

def checkSquare(L, p, N):
  line = p // N
  col = p % N
  v = L[p]
  minLine = line - (line % 3)
  minCol = col - (col % 3)
  for i in range(minLine, line):
    for j in range(minCol, minCol + 3):
      ix = i*N + j
      x = L[ix]
      if x == v:
        return False
  i = line
  for j in range(minCol, col):
    ix = i*N + j
    x = L[ix]
    if x == v:
      return False
  return True

def checkAddition(L, p, N):
  # print checkLine(L, p, N)
  # print checkColumn(L, p, N)
  # print checkSquare(L, p, N)

  return (checkLine(L, p, N)
    and checkColumn(L, p, N)
    and checkSquare(L, p, N))

def placer(L, p, N):
  # print p
  if N*N == p:
    handle(L, N)
  else:
    for x in D(N):
      # print x
      L.append(x)
      if checkAddition(L, p, N):
        placer(L, p+1, N)
      L.pop()

def handle(L, N):
  print ","*N
  for i in range(N):
    for k in range(i*N, (i+1)*N):
      x = L[k]
      print x,
      if k % 3 == 2 and k % N != N-1:
        print "|",
    print
    if i % 3 == 2 and i % N != N-1:
      print "-"*21
    

def D(N):
  return range(1, N+1)




def placer2(L, p, N):
  handle(L, N)
  time.sleep(0.1)
  if N*N == p:
    time.sleep(1)
  else:
    for x in D(N):
      L[p] = x
      if checkAddition(L, p, N):
        placer2(L, p+1, N)
      L[p] = 0

placer2([0]*9*9, 0, 9)