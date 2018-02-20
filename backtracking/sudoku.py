def validPartial(p, L):
  print "p:", p
  if p == 0:
    return True
  if p >= 9 and L[p] == L[p-9]: # second line at least
    return False
  if p % 9 == 0 and not checkFullLine(L[p-9:p]):
    return False
  elif L[p] == L[p - 1]: # two identical values on *same* line
    return False
  if (p//9) % 3 == 2 # lines 3, 6, 9
    and p % 3 == 2: # col 3, 6, 9
    checkSquare(p, L)
  return checkCols(p, M)



# def checkLines(p, M): # p != 0
#   if p % 9 == 0:
#     return checkFullLine(M[(p // 9) - 1])

def checkCols(L):
  for j in range(9):
    return (sum(L[j*9:(j+1)*9]) <= SUM)

SUM = sum(range(1,10))
def checkFullLine(L):
  return (sum(L) == SUM)

def checkSquare(p, L):
  square = []
  for i in range(3):
    square = L[p-2 - 9*i :p+1 - 9*i]
  print "square:", square
  return checkFullLine(square)


def validPartial(p, L):
  if p == 0:
    return True
  checkPartialLine(p, L)

def checkPartialLine(p, L):
  start = (p // 9)*9
  line = L[start:p]
  return isNotIn(L[p], line)