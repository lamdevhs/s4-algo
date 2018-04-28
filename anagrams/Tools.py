from Either import Left, Right


# ----
# ----
# Path -> List String
def linesFromFile(filepath):
  try:
    with open(filepath,'rt') as desc:
      lines = desc.readlines()
      lines = map(str.strip, lines)
  except:
    return Left("Error while trying to read file. probably wrong path")
  return Right(lines)

def linesToFile(lines, filepath):
  try:
    with open(filepath,'wt') as desc:
      lines = map(lambda l: l + "\n", lines)
      desc.writelines(lines)
  except:
    return Left("Error while trying to write file. probably wrong path")
  return Right(None)

def pause(msg = ""):
  raw_input("pause " + msg)

# (x -> Num) .
# List x ->
# Num
def mapsum(f, xs):
  s = 0
  for x in xs:
    s += f(x)
  return s

# x -> x
def identity(x):
  return x


# x . List x -> Int
def indexOf(x, ys):
  for i in range(len(ys)):
    y = ys[i]
    if y == x:
      return i
  return -1

# x . List x -> Int
def indexOf_div(x, ys):
  m = 0
  M = len(ys)
  while m < M - 1:
    c = (M + m)//2
    y = ys[c]
    if y == x:
      return c
    elif x < y:
      M = c
    else:
      m = c
  if ys[m] == x:
    return m
  else:
    return -1

# List x .
# (x -> c) ->
# (List c, List (List x))
def classify(xs, getClass):
  # if xs == None:
  #   return None
  classes = []
  groups = []
  for x in xs:
    cLass = getClass(x)
    classIndex = indexOf(cLass, classes)
    if classIndex == -1:
      classIndex = len(classes)
      classes.append(cLass)
      groups.append([x])
    else:
      groups[classIndex].append(x)
  z = zip(classes, groups)
  z.sort(ff)
  (classes, groups) = unzip(z)
  return (classes, groups)

def ff(t1, t2):
  return cmp(t1[0],t2[0])

def unzip(L):
  l = len(L)
  A = [None]*l
  B = [None]*l
  for ix in range(l):
    (a, b) = L[ix]
    A[ix] = a
    B[ix] = b
  return (A, B)


def nDuplicates(L):
  L = sorted(L)
  n = 0
  for i in range(1,len(L)):
    if L[i] == L[i-1]:
      n += 1
  return n