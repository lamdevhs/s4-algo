
from Tools import (pause, mapsum, linesToFile,
  linesFromFile, dicopath, identity)

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
  def __init__(self, words, verbose = False):
    # self.dico = multigroup(words, [wordHead, len, wordSum])
    if verbose:
      print "building Dico..."
    self.dico = multigroup(words, [len, wordSum])
    if verbose:
      print "grouping done..."

    # set up classes:
    for lenGrp in self.dico:
      if lenGrp != None:
        for i in range(len(lenGrp)):
          sumGrp = lenGrp[i]
          if sumGrp != None:
            lenGrp[i] = classify(sumGrp, sorted)
    
    if verbose:
      print "classifying done..."
      print "Dico done."

  # Path -> Dico
  @staticmethod
  def fromFile(dicopath, verbose = False):
    eith = linesFromFile(dicopath)
    if eith.isLeft:
      raise Exception (eith.leftValue)
    words = eith.rightValue
    D = Dico(words, verbose)
    return D

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
  def multiAnagrams(self, inputString, numberOfWords):
    # minLen = 1
    # (letters, grouped) = classify(string, identity)
    # amounts = map(len, grouped)
    # print letters, amounts
    # self.backtracker(NW, NC, minLen,
    #   letters, amounts, "", 0, 0, 0,
    #   solutions, [])
    solutions = []
    S = BTState(solutions, numberOfWords,
      inputString)
    self.backtracker(S)
    return solutions

  # Dico . BTState -> Void
  def backtracker(self, S):
    # self, NW, NC, minLen,
    # letters, amounts,
    # selection, selLen, Len, whichLetter,
    # solutions, partialSolution):
    if S.nWordsLeft == 0:
      # print "NW = 0"
      return # solutions
    elif S.nWordsLeft == 1:
      # print "NW = 1"
      S.selection = rebuildString(S.validLetters,
        S.validAmounts)
      S.selLen = len(S.selection)
      if (S.prevWord != None and
        S.selLen == len(S.prevWord) and
        S.selection < S.prevWord):
        return # deadend

      anagrams = self.anagramsOf(S.selection)
      if len(anagrams) != 0:
        # print "anagrams != 0"
        S.result.append(S.partialSolution
          + [anagrams])
        # print "sol len ----", len(solutions)
      else:
        # print "anagrams == 0"
        pass
    else:
      if S.nextWordLen == None:
        # print "Len == 0"
        minL = S.minLenNextWord
        maxL = S.nLettersLeft // S.nWordsLeft
        for L in range(minL, 1 + maxL):
          newS = S.copy()
          newS.nextWordLen = L
          newS.selection = ""
          newS.selLen = 0
          newS.nextLetterIx = 0
          self.backtracker(newS)
          # self.backtracker(NW, NC, minLen,
          #   letters, amounts, "", 0, L, 0,
          #   solutions, partialSolution)
      else:
        # print "Len =", Len
        if S.selLen == S.nextWordLen:
          # print "selLen == Len"
          if (S.prevWord != None and
            S.selLen == len(S.prevWord) and
            S.selection < S.prevWord):
            return # deadend
          anagrams = self.anagramsOf(S.selection)
          if len(anagrams) != 0:
            newS = S.copy()
            newS.nWordsLeft -= 1
            newS.minLenNextWord = S.selLen
            newS.prevWord = S.selection
            newS.nextWordLen = None
            newS.partialSolution = (S.partialSolution
              + [anagrams])
            self.backtracker(newS)
            # self.backtracker(NW - 1, NC, selLen,
            #   letters, amounts, "", 0, 0, 0,
            #   solutions, partialSolution + [anagrams])
        else:
          # print "selLen != Len", Len, selLen, whichLetter
          if S.nextLetterIx >= len(S.validLetters):
            return # wrong path
          letter = S.validLetters[S.nextLetterIx]
          maxAmount = S.validAmounts[S.nextLetterIx]
          maxQ = min(S.nextWordLen-S.selLen, maxAmount)
          for quantity in range(0, maxQ + 1):
            # print "quantity", quantity, letter
            S.validAmounts[S.nextLetterIx] -= quantity
            newS = S.copy()
            newS.selection = (S.selection
              + quantity*letter)
            newS.selLen += quantity
            newS.nLettersLeft -= quantity
            newS.nextLetterIx += 1
            self.backtracker(newS)
            S.validAmounts[S.nextLetterIx] += quantity
            # ^ S and newS share the same .amounts
            # array, so we have to reset its values
            # after backtracking

            # self.backtracker(NW, NC - quantity, minLen,
            #   letters, amounts,
            #   selection + quantity*letter,
            #   selLen + quantity, Len, whichLetter + 1,
            #   solutions, partialSolution)



class BTState():
    # (self, nWordsLeft, nLettersLeft,
    # minLenNextWord,  nextWordLen,
    # validLetters, validAmounts,
    # selection, selLen, nextLetterIx,
    # partialSolution):
  def __init__(self, result, numberOfWords = None,
      inputString = ""):
    self.nWordsLeft = numberOfWords

    inputString = sorted(inputString)
    self.nLettersLeft = len(inputString)
    
    (validLetters, groupedByLetter) = classify(
      inputString, identity)
    self.validLetters = validLetters
    self.validAmounts = map(len, groupedByLetter)
    
    self.minLenNextWord = 1
    self.nextWordLen = None
    self.prevWord = None
    self.selection = ""
    self.selLen = 0
    self.nextLetterIx = 0
    self.partialSolution = []
    self.result = result

  # BTState -> BTState
  def copy(self):
    r = BTState(self.result) # mostly dummy state
    (r.nWordsLeft,
      r.nLettersLeft,
      r.validLetters,
      r.validAmounts,
      r.minLenNextWord,
      r.nextWordLen,
      r.prevWord,
      r.selection,
      r.selLen,
      r.nextLetterIx,
      r.partialSolution) = (self.nWordsLeft,
      self.nLettersLeft,
      self.validLetters,
      self.validAmounts, # this array is not cloned
      self.minLenNextWord,
      self.nextWordLen,
      self.prevWord,
      self.selection,
      self.selLen,
      self.nextLetterIx,
      self.partialSolution)
        # ^ this array is not cloned either
    return r




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

# if sol[0] == sol[1]:
#       rest = mult(sol[2:])
#       for i in range(len(head)):
#         for j in range(i + 1, len(head)):
#           for y in rest:
#             r.append([])

def mult1(sol):
  if len(sol) != 2 or sol[0] < 0:
    raise Exception("mult1(): aberrant input")
  N = sol[0]
  family = sol[1]
  r = []
  bt(N, family, r, last = 0)
  return r

def bt(N, family, r, last, partial = []):
  if N == 0:
    r.append(partial)
    return
  else:
    for i in range(last, len(family)):
      val = family[i]
      bt(N-1, family, r, i, partial + [val])


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
  r = map(sorted, r)
  r = map(lambda a: Join(a, " "), r)
  return r

# String . String -> Bool
def areAnagrams(wa, wb):
  return sorted(wa) == sorted(wb)

def testvalid(D, string, n):
  print "test", string, n
  res = D.multiAnagrams(string, n)
  print res
  flat = flatten(res)
  print "dup?", len(dup(flat))
  print "reslen=", len(flat)
  linesToFile(flat, "A" + string + str(n) + ".tempo")

def main():
  D = Dico.fromFile(dicopath, verbose = True)
  #testvalid(D, "CHAMPOLLION", 2)
  testvalid(D, "AIRAIR", 2)
  #testvalid(D, "CHAMPOLLION", 4)
  #testvalid(D, "CHAMPOLLION", 1)
  #testvalid(D, "CHAMPOLION", 3)
  #testvalid(D, "CHAMPOLION", 4)
main()