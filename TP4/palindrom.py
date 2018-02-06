from random import choice, randrange

# ---------------- version brut
def brutPalin(cs):
  pos = 0
  length = 1
  for i in range(len(cs)):
    for j in range(i+1, len(cs)+1):
      hereLen = j - i
      if (isPalin(cs, i, j)) and hereLen > length:
        pos = i
        length = hereLen
  return (pos, length)

def isPalin(cs, i, j):
  j -= 1
  while i <= j:
    if cs[i] != cs[j]:
      return False
    i+=1
    j-=1
  return True


# --------------- matricielle

def matrixPalin(cs):
  pos = 0
  length = 1
  ln = len(cs)
  M = [[False for i in range(ln)] for j in range(ln)]
  
  for i in range(ln):
    M[i][i] = True
    if i != ln -1:
      if cs[i] == cs[i+1]:
        M[i][i+1] = True
        if length < 2:
          pos = i
          length = 2 

  for L in range(3, ln + 1):
    for i in range(ln):
      j = i + L - 1
      if j < ln: # otherwise end of the diagonal
        # we're at M[i][j]:
        if M[i+1][j-1] and cs[i] == cs[j]:
          M[i][j] = True
          if length < L:
            pos = i
            length = L
  return (pos, length)

# v3

def v3(cs):
  fullLen = len(cs)
  # result:
  resLen = 1
  resPos = 0
  centers = 2*fullLen - 1
    # center 0 is char 0, center 1 is between
    # char 0 and 1, center 2 is char 1, etc

  for center in range(centers): # searching left to right
    if center % 2 == 0: # impair palyndroms
      # there're `center/2` characters to the left
      # and `fullLen - center - 1` chars to the right
      # of this center
      leftLen = center / 2
      rightLen = fullLen - leftLen - 1
      hopefulLen = 1 + 2*min(leftLen, rightLen)
        # ^ max palindrom len we can hope for this center

    else: # center % 2 != 0 <--> pair palindroms
      leftLen = 1 + ((center - 1) / 2)
      rightLen = fullLen - leftLen
      hopefulLen = 2*min(leftLen, rightLen)

    if hopefulLen > resLen:
      # no point continuing otherwise
      # (using a `break` would be more efficient...)
      (posHere, maxLenHere) = biggestPalinHere(cs, center, hopefulLen)
      if maxLenHere > resLen:
        resLen = maxLenHere
        resPos = posHere
  return (resPos, resLen)


def biggestPalinHere(cs, center, hope):
  if center % 2 == 0: # impair palindrom
    i = (center / 2) - 1
    j = i + 2
    halfHope = (hope - 1) / 2
    toAdd = 1

  else: # pair palindrom
    i = (center - 1) / 2
    j = i + 1
    halfHope = hope / 2
    toAdd = 0

  for offset in range(halfHope):
    if cs[i - offset] != cs[j + offset]:
      return (i - offset + 1, offset*2 + toAdd)
  return (i - halfHope + 1, hope)

  # the output is slightly absurd in the case of
  # zero-lengthed pair palindroms, but who cares






def getStr(filename):
  with file(filename) as f:
    return f.read()

path = "plp/"
files = [
  "plp_" + str(x) + ".txt"
  for x in [500,1000,2000,4000,8000]
  ]

def testWithFiles(f):
  for fileName in files:
    cs = getStr(path + fileName)
    print "file:", fileName
    print f(cs)
    print

AZ = "abcdefghijklmnopqrstuvwxyz"

def compare(f, g):
  pb = False
  for _ in range(1000):
    size = randrange(100)
    cs = [choice(AZ) for c in range(size)]
    resf = f(cs)
    resg = g(cs)
    if resf != resg:
      pb = True
      print "Houston, we have a problem"
      print size, ":", cs
      print "f", resf
      print "g", resg
  if not pb:
    print 'all ok'

#testFiles(brutPalin)


compare(brutPalin, matrixPalin)
compare(brutPalin, v3)


testWithFiles(matrixPalin)
testWithFiles(v3)