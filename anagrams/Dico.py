
import sys
from Tools import (mapsum, indexOf_div,
  linesFromFile, classify, indexOf)

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


class Dico():
  # Dico . List String -> Dico
  def __init__(self, words, verbose = False):
    # self.dico = multigroup(words, [wordHead, len, wordSum])
    if verbose:
      print "building Dico..."
    self.dico = multigroup(words, [len, wordSum])
    if verbose:
      print "indexing done."

    # set up families:
    if verbose:
      sys.stdout.write("creating families... ")
      sys.stdout.flush()
    for lenGrp in self.dico:
      if verbose:
        sys.stdout.write("#")
        sys.stdout.flush()
      if lenGrp != None:
        for i in range(len(lenGrp)):
          sumGrp = lenGrp[i]
          if sumGrp != None:
            lenGrp[i] = classify(sumGrp, sorted)
    
    if verbose:
      print
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
    ix = indexOf_div(cLass, classes)
    if ix == -1:
      return [] # ?? or None?
    else:
      return groups[ix][:]

        # # Dico . String -> Int
        # def nbAnagramsOf(self, word):
        #   L = len(word)
        #   if L >= len(self.dico):
        #     return 0
        #   lenGrp = self.dico[L]
        #   if lenGrp == None:
        #     return 0
          
        #   S = wordSum(word)
        #   if S >= len(lenGrp):
        #     return 0
        #   sumGrp = lenGrp[S]
        #   if sumGrp == None:
        #     return 0
          
        #   (classes, groups) = sumGrp
        #   cLass = sorted(word)
        #   ix = indexOf(cLass, classes)
        #   if ix == -1:
        #     return 0 # ?? or None?
        #   else:
        #     return len(groups[ix])

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



# ----
# String
dicopath = "dico.txt"

# The one and only dictionnary, used to get very fast
# access to any word's families of known anagrams.
# Is imported by the other files as global variable.
#
# Dico
DICO = Dico.fromFile(dicopath, verbose = True)

if True:
  no = 0
  NN = 0
  for L in range(len(DICO.dico)):
    d1 = DICO.dico[L]
    if d1 != None:
      for S in range(len(d1)):
        d2 = d1[S]
        if d2 != None:
          (sigs, families) = d2
          no += 1
          for fam in families:
            NN += len(fam)
          if sorted(sigs) != sigs:
            no += 1
  print "no", no, NN
