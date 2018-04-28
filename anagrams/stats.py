
from Either import Left, Right

# ----
# ----
dicopath = "dico.txt"

# ----
# ----
def contentFromFile(filepath):
  try:
    with open(filepath,'rt') as desc:
      allLines = desc.readlines()
  except:
    return Left("Error while trying to read file. probably wrong path")
  return Right(allLines)


# ----
# Path -> Either Message (List String)
def dicoFromFile(dicopath):
  eith = contentFromFile(dicopath)
  if eith.isLeft:
    return eith
  lines = eith.rightValue
  r = map(str.strip, lines)
  # r = []
  # for line in lines:
  #   r.append(line.strip())
  return Right(r)

#   List x
# . (x -> Int)
# -> Array (List x)
def group(xs, f):
  r = []
  for x in xs :
    n = f(x)
    if len(r) <= n:
      grow(r, n)
    # if r[n] == :
    #   r[n] = []
    r[n].append(x)
  return r

# Array (List a) -> Array (List a) [mutate]
def grow(xs, n):
  length = len(xs)
  while length <= n:
    length += 1
    xs.append([])
  return xs

def letter2int(char):
  return ord(char) - ord('A') + 1


def wordSum(word):
  return sum(map(letter2int, word))

def wordSum2(word):
  return (sum(map(letter2int, word))
    + letter2int(word[0])*100)

#   List x
# . (x -> Int)
# . (x -> Int)
# -> Array (Array (List x))
def group2D(xs, fa, fb):
  ra = group(xs, fa)
  r = []
  for g in ra:
    r.append(group(g, fb))
  return r

# List (List a) -> Int
def maxlen(xss):
  lens = map(len, xss)
  if len(lens) == 0:
    return 0
  return max(lens)

# List (List a) -> Int
def holes(xss):
  lens = map(len, xss)
  if len(lens) == 0:
    return 0
  isZero = lambda n: n == 0
  return len(filter(isZero, lens))

# List (List a) -> List Int
def lenstats(xss):
  freqs = [0]*20
  lens = map(len, xss)
  if len(lens) == 0:
    return freqs
  for n in lens:
    freqs[n//10] += 1
  return freqs

# List (List Int) -> List Int
def zipsum(xss):
  if len(xss) == 0:
    return []
  N = len(xss[0])
  r = [0]*N
  for i in range(N):
    for j in range(len(xss)):
      r[i] += xss[j][i]
  return r

#   List x
# . (x -> Int)
# . (x -> Int)
# . (x -> Int)
# -> Array (Array (Array (List x)))
def group3D(xs, fa, fb, fc):
  ra = group(xs, fa)
  r = []
  for g in ra:
    r.append(group2D(g, fb, fc))
  return r

# List x -> x
def wordHead(xs):
  return letter2int(xs[0])


def stats(xss, nwords, name):
  print 
  print "----- stats for", name
  freqsums = zipsum(map(lenstats, xss))
  print freqsums
  total = 0
  for j in range(len(freqsums)):
    n = freqsums[j]
    i = (j+1)*10
    freq = n*i/float(nwords)
    print i, n, freq
    total += freq
  print "total:", total

def maxn(xs):
  if len(xs) == 0:
    return 0
  return max(xs)

def indexOf(x, ys):
  for i in range(len(ys)):
    y = ys[i]
    if y == x:
      return i
  return -1

def classify(words, getClass):
  classes = []
  groups = []
  for word in words:
    cLass = getClass(word)
    classIndex = indexOf(cLass, classes)
    if classIndex == -1:
      classIndex = len(classes)
      classes.append(cLass)
      groups.append([word])
    else:
      groups[classIndex].append(word)
  return (classes, groups)

# List (List (List z) -> (z -> r) -> LLL r
def map3(f, xsss):
  rsss = []
  for xss in xsss: # each letter
    rss = []
    for xs in xss: # each length
      rs = []
      for x in xs: # each word sum group
        rs.append(f(x))
      rss.append(rs)
    rsss.append(rss)
  return rsss


def main():
  eith = dicoFromFile(dicopath)
  if eith.isLeft:
    print eith.leftValue
    return
  words = eith.rightValue
  nwords = len(words)
  lengths = map(len, words)
  maxsize = max(lengths)
  minsize = min(lengths)
  groups = group(words, len)
  glengths = map(len, groups)
  print glengths
  gsums = group(words, wordSum)
  gsumlens = map(len, gsums)
  print len(gsumlens)
  #print gsums[245][0]
  gg = group2D(words, len, wordSum2)
  ggmaxlens = map(maxlen, gg)
  print ggmaxlens
  print sum(map(holes, gg))
  print map(lenstats, gg)
  #print sum(map(letter2int, gsums[245][0]))
  #print sum(map(letter2int, "ZOO"))
  #stats(gg, nwords, "group2D")

  ggg = group3D(words, wordHead, len, wordSum)
  if False:
    #print map(maxlen, ggg)
    print len(ggg)
    for i in range(len(ggg)):
      gg = ggg[i]
      stats(gg, nwords, "group3D " + str(i))
    print "lengths:", map(len, ggg)
    print ggg[25][15]

  maxlen3 = max(map(
    lambda gg: maxn(map(maxlen, gg)),
    ggg))
  print maxlen3
  map3(lambda ws: classify(ws, sorted), ggg)

#main()

def main2():
  eith = dicoFromFile(dicopath)
  if eith.isLeft:
    print eith.leftValue
    return
  words = eith.rightValue
  nwords = len(words)
  aaa = [0]*200
  A = ord('A')
  Z = ord('Z')
  for i in range(len(words)):
    word = words[i]
    askii = map(ord, word)
    m = min(askii)
    M = max(askii)
    if m < A or M > Z:
      print i, word
    for letter in word:
      aaa[ord(letter)] += 1
  print "done"
  print aaa
main2()