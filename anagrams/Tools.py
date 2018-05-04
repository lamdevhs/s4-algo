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

# Counts the number of duplicate
# values in a list.
#
# Probably not very efficient
# but it's enough for what is being done with it.
# e.g.:
# . nDuplicates([x,y,z]) == 0
# . nDuplicates([x,x,y,y,y,z]) == len([x,y,y]) == 3 
# In terms of sets:
# . nDuplicates(L) == len(L) - len(list(set(L)))
#
# List x -> Int
def nDuplicates(L):
  L = sorted(L)
  n = 0
  for i in range(1,len(L)):
    if L[i] == L[i-1]:
      n += 1
  return n

# Exhaustive, basic search of x
# in a list `ys` which isn't expected
# to be sorted.
#
# x . List x -> Int
def indexOf(x, ys):
  for i in range(len(ys)):
    y = ys[i]
    if y == x:
      return i
  return -1

# Takes a list xs and a function f.
# Returns two lists in a tuple.
# The first list is the *set* of all
# images of all elements of that
# list by the given function.
# The second list contains all the preimage sets
# that correspond.
# Mathematically:
# classify([x,y,z,...], f: A -> B) = ({a,b,...}, [f^-1(a), f^-1(b), ...])
#     with (x,y,z in A) and (a,b,... in B) and (f^-1(a) subset of A)
# (It isn't exactly that because there can be repetitions of values
# in f^-1(a), if the same value exists more than once in the input
# list.)
#
# e.g.:
# . classify([3,2,1,2,3], f(x) := 10*x)
#     = ([30,20,10], [[3,3],[2,2],[1]])
# . classify([xyz,abc,def,axy], first_element)
#     = ([x,a,d], [[xyz],[abc,axy],[def]])
#
# List x .
# (x -> c) ->
# (List c, List (List x))
def classify(xs, f):
  # if xs == None:
  #   return None
  classes = []
  groups = []
  for x in xs:
    cLass = f(x)
    classIndex = indexOf(cLass, classes)
    if classIndex == -1:
      classIndex = len(classes)
      classes.append(cLass)
      groups.append([x])
    else:
      groups[classIndex].append(x)
  return (classes, groups)


# Divide-and-Conquer algorithm,
# to be used on a previously sorted
# list of course.
#
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

# Does what classify() does, except
# the output is sorted, based on the list of images
# by f (the first list of the output tuple).
# e.g.:
# . classify_div([bca,aba,cab,caa], sorted)
#   == ([aab,aac,abc], [[aba],[caa],[bca,cab])
# we do have here aab < aac < abc
# by contrast:
# . classify([bca,aba,cab,caa], sorted)
#   == ([abc,aab,aac], [[bca,cab],[aba],[caa])
# and here, the classes [abc, aab, aac] aren't sorted
# since abc > aab.
#
# The purpose is to increase the speed of searching
# through that double list, via a divide-and-conquer
# algorithm over the leftwise list of the output.
#
# List x .
# (x -> c) ->
# (List c, List (List x))
def classify_div(xs, f):
  # if xs == None:
  #   return None
  classes = []
  groups = []
  for x in xs:
    cLass = f(x)
    classIndex = indexOf(cLass, classes)
    if classIndex == -1:
      classIndex = len(classes)
      classes.append(cLass)
      groups.append([x])
    else:
      groups[classIndex].append(x)
  z = zip(classes, groups)
  z.sort(leftSorting)
  (classes, groups) = unzip(z)
  return (classes, groups)

# Compares both tuples based on
# the left value of each tuple.
#
# (s, a) . (s, b) -> {-1,1,0}
def leftSorting(t1, t2):
  return cmp(t1[0],t2[0])

# List (a, b) -> (List a, List b)
def unzip(L):
  l = len(L)
  A = [None]*l
  B = [None]*l
  for ix in range(l):
    (a, b) = L[ix]
    A[ix] = a
    B[ix] = b
  return (A, B)
