from Either import Left, Right

# ----
# ----
dicopath = "dico.txt"

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
  return (classes, groups)
