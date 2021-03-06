from random import choice, randrange
import time

# --------------- version brut
def brutPalin(cs):
  if len(cs) == 0:
    return (-1, 0)

  resPosition = 0
  resLength = 1
  for i in range(len(cs)):
    for j in range(i+1, len(cs)+1):
      hereLen = j - i
      if (isPalin(cs, i, j)) and hereLen > resLength:
        resPosition = i
        resLength = hereLen
  return (resPosition, resLength)

def isPalin(cs, i, j):
  j -= 1
  cont = True
  result = True
  while i <= j and cont:
    if cs[i] != cs[j]:
      result = False
      cont = False # to break the loop
    i+=1
    j-=1
  return result


# --------------- varsion matricielle

def matrixPalin(cs):
  if len(cs) == 0:
    return (-1, 0)

  resPosition = 0
  resLength = 1
  ln = len(cs)
  M = [[False for i in range(ln)] for j in range(ln)]
  
  for i in range(ln):
    M[i][i] = True
    if i != ln -1:
      if cs[i] == cs[i+1]:
        M[i][i+1] = True
        if resLength < 2:
          resPosition = i
          resLength = 2 

  for L in range(3, ln + 1):
    for i in range(ln):
      j = i + L - 1
      if j < ln: # otherwise end of the diagonal
        # we're at M[i][j]:
        if M[i+1][j-1] and cs[i] == cs[j]:
          M[i][j] = True
          if resLength < L:
            resPosition = i
            resLength = L
  return (resPosition, resLength)

# --------------- v3

def v3(cs):
  fullLen = len(cs)

  if fullLen == 0:
    return (-1, 0)
  # result:
  resPos = 0
  resLen = 1

  # total amount of centers:
  centers = 2*fullLen - 1
    # center 0 is cs[0],
    # center 1 is between cs[0] and cs[1],
    # center 2 is cs[1], etc
    # thus, palindromes with even centers are odd-sized,
    # those with odd centers are even-sized.

  for center in range(centers): # searching left to right
    if center % 2 == 0: # odd-sized palindroms
      # there're `center/2` characters to the left
      # and `fullLen - center - 1` chars to the right
      # of this center
      # (the char right "under" the center isn't taken into account)
      leftLen = center / 2
      rightLen = fullLen - leftLen - 1
      hopefulLen = 1 + 2*min(leftLen, rightLen)
        # ^ max palindrom len we can hope for this center

    else: # center % 2 != 0 <--> pair palindroms
      leftLen = 1 + ((center - 1) / 2)
      rightLen = fullLen - leftLen
      hopefulLen = 2*min(leftLen, rightLen)

    if hopefulLen > resLen:
      # ^ no point continuing if we can't hope
      # for a longer palindrom
      # than what we found previously
      # (using a `break` here would be more efficient...)
      (posHere, maxLenHere) = biggestPalinHere(cs, center, hopefulLen)
      if maxLenHere > resLen: # did we find better here?
        resLen = maxLenHere
        resPos = posHere
  return (resPos, resLen)


def biggestPalinHere(cs, center, hope):
  if center % 2 == 0:
    # palindromes de taille impair:
    # eg center = 0 correspond a celui
    # centre sur cs[0]
    i = (center / 2) - 1
    j = i + 2
    halfHope = (hope - 1) / 2
    toAdd = 1
      # ^ we add the char under the center
      # to the final length of the palin

  else:
    # palindromes de taille pair
    # eg center = 1 correspond a celui
    # centre sur la faille entre cs[0] et cs[1]
    i = (center - 1) / 2
    j = i + 1
    halfHope = hope / 2
    toAdd = 0

  for k in range(halfHope):
    if cs[i - k] != cs[j + k]:
      # ^ end of palindrom detected
      return (i - k + 1, k*2 + toAdd)
  return (i - halfHope + 1, hope)


# this algorithm finds the last biggest
# palindrom, so we gotta apply it to reversed
# strings to get the same result
# obviously it could be seen as a disadvantage
# when comparing benchmarks, but this algorithm
# remains faster than the others anyway
def manacher(original):
  s = reversed(original)
  if s == "":
    t = "^#$"
  else:
    t = "^#" + "#".join(s) + "#$"

  c = 0
  r = 0
  p = [0] * len(t)
  for i in range(1,len(t)-1):
    mirror = 2*c - i
    p[i] = max(0, min(r-i, p[mirror]))

    while t[i+1+p[i]] == t[i-1-p[i]]:
      p[i] += 1

    if i+p[i] > r:
      c = i
      r = i+p[i]

  (k,i) = max((p[i],i) for i in range(1,len(t)-1))
  return (len(original) - (i+k)/2, k)




def strFromFile(path):
  with file(path) as f:
    return f.read()

path = "plp/"
files = [
  "plp_" + str(x) + ".txt"
  for x in [500,1000,2000,4000,8000]
  ]

# also prints the benchmarking
def testWithFiles(fs):
  for f in fs:
    print f.func_name + "():"
    for fileName in files:
      cs = strFromFile(path + fileName)
      before = time.clock()
      res = f(cs)
      elapsed = time.clock() - before;
      print "  file", fileName, "->", res
      print "    time elapsed:", elapsed
  print

AZ = "abcdefghijklmnopqrstuvwxyz"

#| check if results from f and g are identical
#| test them over a wide range of different inputs
def compare(f, g):
  print "comparing", f.func_name, g.func_name, ":"
  pb = False
  for _ in range(1000):
    size = randrange(100)
    cs = [choice(AZ) for c in range(size)]
    resf = f(cs)
    resg = g(cs)
    if resf != resg:
      pb = True
      print "Houston, we have a problem!"
      print "size =", size, "; input =", cs
      print "results:"
      print f.func_name, resf
      print g.func_name, resg
  if not pb:
    print 'results are identical'
  print

testWithFiles([brutPalin, matrixPalin,v3, manacher])

compare(manacher, v3)
compare(brutPalin, matrixPalin)
compare(brutPalin, v3)





