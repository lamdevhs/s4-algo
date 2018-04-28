
from Tools import pause, mapsum, linesToFile, linesFromFile, dicopath, identity

# Char -> Int
def letter2int(char):
  return ord(char) - ord('A') + 1

# String -> Int
def wordHead(string):
  return letter2int(string[0])

zed = letter2int('Z')

# String -> Int
def wordSum(word):
  #return mapsum(letter2int, word)
  letters = sorted(word)
    # ^ TODO: maybe find a way not to do it twice
  A = letter2int(letters[0])
  Z = letter2int(letters[-1])
  return (mapsum(letter2int, word)
    + (A + Z)*7)

# List (List a) ->
# List (List a) [mutate]
def grow(xs, n):
  length = len(xs)
  while length <= n:
    length += 1
    xs.append(None)
  return xs

# List x .
# (x -> Int) ->
# List (List x)
def group(xs, f):
  if xs == None:
    return None
  r = []
  for x in xs:
    key = f(x)
    if len(r) <= key:
      grow(r, key)
    if r[key] == None:
      r[key] = []
    r[key].append(x)
  return r

# List x .
# List (x -> Int) ->
# List (... (List x)...)
# TODO: optimise for in-place mutation if possible
def multigroup(xs, fs):
  if xs == None:
    return None

  if len(fs) == 0:
    return xs
  else:
    f = fs[0]
    gs = group(xs, f)
    r = []
    for g in gs:
      r.append(multigroup(g, fs[1:]))
    return r

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

def rebuildString(letters, amounts):
  r = ""
  for i in range(len(letters)):
    r += letters[i]*amounts[i]
  return r

class Dico():
  # Dico . List String -> Dico
  def __init__(self, words):
    # self.dico = multigroup(words, [wordHead, len, wordSum])
    print "building Dico..."
    self.dico = multigroup(words, [len, wordSum])
    print "grouping done..."
    # set up classes:
    #for letterGrp in self.dico:
    #  if letterGrp != None:
    for lenGrp in self.dico:
      if lenGrp != None:
        for i in range(len(lenGrp)):
          sumGrp = lenGrp[i]
          if sumGrp != None:
            lenGrp[i] = classify(sumGrp, sorted)
    print "classifying done..."
    print "Dico done."

  # Dico . String -> List String
  def anagramsOf(self, word):
    L = len(word)
    if L >= len(self.dico):
      return []
    lenGrp = self.dico[L]
    if lenGrp == None:
      return []
    
    S = wordSum(word)
    if S >= len(lenGrp):
      return []
    sumGrp = lenGrp[S]
    if sumGrp == None:
      return []
    
    (classes, groups) = sumGrp
    cLass = sorted(word)
    ix = indexOf(cLass, classes)
    if ix == -1:
      return [] # ?? or None?
    else:
      return groups[ix]

  # Dico . Int ->
  # (Int, List (List String))
  def bestOfLength(self, L):
    if len(self.dico) <= L or L < 0:
      return (0, [])
    subdico = self.dico[L]
    if subdico == None:
      return (0, [])
    maxAmount = 0
    results = []
    for sumGrp in subdico:
      if sumGrp != None:
        (classes, wordgroups) = sumGrp
        for classIx in range(len(classes)):
          wgrp = wordgroups[classIx]
          N = len(wgrp)
          if N > maxAmount:
            maxAmount = N
            results = [wgrp[:]]
          elif N == maxAmount:
            results.append(wgrp[:])
    return (maxAmount, results)

  # Dico ->
  # (Int, List (List String))
  def bestOfAll(self):
    currentBest = (0, [])
    for L in range(len(self.dico)):
      best = self.bestOfLength(L)
      if currentBest[0] < best[0]:
        currentBest = best
      elif currentBest[0] == best[0]:
        currentBest = (best[0],
          currentBest[1] + best[1])
    return currentBest

  # Dico . String ->
  # List (List String)
  def A1(self, letters):
    r = []
    for L in range(len(self.dico)):
      r += self.multiAnagramsOfLen(letters, L)
    return r

  # Dico . String . Int ->
  # List (List String)
  def multiAnagrams(self, string, NW):
    string = sorted(string)
    NC = len(string)
    minLen = 1
    (letters, grouped) = classify(string, identity)
    amounts = map(len, grouped)
    print letters, amounts
    solutions = []
    self.backtracker(NW, NC, minLen,
      letters, amounts, "", 0, 0, 0,
      solutions, [])
    return solutions

  def backtracker(
    self, NW, NC, minLen,
    letters, amounts,
    selection, selLen, Len, whichLetter,
    solutions, partialSolution):
    if NW == 0:
      # print "NW = 0"
      return # solutions
    elif NW == 1:
      # print "NW = 1"
      string = rebuildString(letters, amounts)
      anagrams = self.anagramsOf(string)
      if len(anagrams) != 0:
        # print "anagrams != 0"
        solutions.append(partialSolution
          + [anagrams])
        # print "sol len ----", len(solutions)
      else:
        # print "anagrams == 0"
        pass
    else:
      if Len == 0:
        # print "Len == 0"
        for L in range(minLen, 1 + NC//NW):
          self.backtracker(NW, NC, minLen,
            letters, amounts, "", 0, L, 0,
            solutions, partialSolution)
      else:
        # print "Len =", Len
        if selLen == Len:
          # print "selLen == Len"
          anagrams = self.anagramsOf(selection)
          if len(anagrams) != 0:
            self.backtracker(NW - 1, NC, selLen,
              letters, amounts, "", 0, 0, 0,
              solutions, partialSolution + [anagrams])
        else:
          # print "selLen != Len", Len, selLen, whichLetter
          if whichLetter >= len(letters):
            return # wrong path
          letter = letters[whichLetter]
          amount = amounts[whichLetter]
          for quantity in range(0, min(Len - selLen, amount) + 1):
            # print "quantity", quantity, letter
            amounts[whichLetter] -= quantity
            self.backtracker(NW, NC - quantity, minLen,
              letters, amounts, selection + quantity*letter,
              selLen + quantity, Len, whichLetter + 1,
              solutions, partialSolution)
            amounts[whichLetter] += quantity





    #FWL = 


def dup(l):
  r = []
  for i in range(len(l)):
    for j in range(i + 1, len(l)):
      if l[i] == l[j]:
        r.append(l[i])
  return r

# List (List String) ->
# List (String)
def mult(sol):
  if len(sol) == 0:
    return []
  if len(sol) == 1:
    return map(lambda s: [s], sol[0])
  else:
    r = []
    head = sol[0]
    rest = mult(sol[1:])
    for x in head:
      for y in rest:
        r.append([x] + y)
    return r


def Join(xs, x):
  if len(xs) == 0:
    return ""
  r = xs[0]
  for i in range(1, len(xs)):
    r += " " + xs[i]
  return r

def flatten(res):
  r = []
  for sol in res:
    r += mult(sol)
    # for x in sol[0]:
    #   for y in sol[1]:
    #     r.append(x + " " + y)
  r = map(sorted, r)
  r = map(lambda a: Join(a, " "), r)
  return r

# String . String -> Bool
def areAnagrams(wa, wb):
  return sorted(wa) == sorted(wb)



def testvalid(D, string, n):
  print "test", string, n
  res = D.multiAnagrams(string, n)
  flat = flatten(res)
  #print "dup?", len(dup(flat))
  print "reslen=", len(flat)
  linesToFile(flat, "AAAA" + string + str(n))

def main():
  eith = linesFromFile(dicopath)
  if eith.isLeft:
    print eith.leftValue
    return
  words = eith.rightValue
  D = Dico(words)
      # print D.anagramsOf("AIR")
      # print D.anagramsOf("TSAR")
      # print D.anagramsOf("SALI")
      # print D.anagramsOf("RUSE")
      # print D.bestOfLength(2)
      # print D.bestOfLength(3)
      # print D.bestOfLength(4)
      # print D.bestOfAll()
      # print rebuildString("aze", [1,2,6])
      # pause()
      # res = D.multiAnagrams("AIRTSARSALI", 3)
      # print len(res)
      # print dup(res)
      # flat = flatten(res)
      # flat.sort()
      # print len(flat)
  # print ("ix", indexOf("AIOLI CONFRATERNEL", flat),
  #   indexOf("FINALE CORRELATION", flat))
  # count = 0
  # for sol in res:
  #   count += len(sol[0])*len(sol[1])
  # print count
  # print areAnagrams("AIOLICONFRATERNEL", "CAROLINEETFLORIAN")

  # if False: # testing how many tests are doable
  #   for k in range(10):
  #     p = pow(10, k)
  #     raw_input("pause ");
  #     print "pow", k, p
  #     for i in range(p):
  #       a = D.anagramsOf("RUSE")
  # pause("and now")
  
  testvalid(D, "CHAMPOLLION", 2)
  testvalid(D, "CHAMPOLION", 3)
  testvalid(D, "CHAMPOLLION", 3)
  testvalid(D, "CHAMPOLION", 4)
  testvalid(D, "CHAMPOLLION", 4)
  testvalid(D, "CHAMPOLLION", 1)

  testvalid(D, "AIRAIR", 2)
  testvalid(D, "AIRAIRFEUFEU", 4)

  #testvalid(D, "CAROLINEETFLORIAN", 3)
  # #print flat
  # linesToFile(flat, "foobbbb")
main()