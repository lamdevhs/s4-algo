
import sys
from Tools import (mapsum, indexOf_div,
  linesFromFile, classify, indexOf)

# Takes a character c, returns:
# - 1 if c == A,
# - 2 if c == B,
# etc.
#
# Char -> Int
def letter2int(char):
  return ord(char) - ord('A') + 1

# More or less returns the sum of the letters of
# the given input, with A = 1, B = 2, etc.
# (The actual formula is a bit different because i noticed
# it made the access process slightly faster.)
#
# String -> Int
def wordSum(word):
  sortedLetters = sorted(word)
  smallest = letter2int(sortedLetters[0])
  biggest = letter2int(sortedLetters[-1])
  return (mapsum(letter2int, word)
    + (smallest + biggest)*7)

# Mutates an array by appending dummy elements
# until the length of the array is at least equal
# to `n + 1`, aka until the index xs[n] is not out
# of bounds.
#
# List (List a) ->
# List (List a) [mutate]
def grow(xs, n):
  length = len(xs)
  while length <= n:
    length += 1
    xs.append(None)
  return xs

# Takes a list xs and a function f.
# Returns an array containing lists of
# elements which share the same image wrt
# the function f. The index of those sublists
# is the very image by f of any element in it.
#
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

# Takes a list `xs`, and a list of functions `fs`.
# Each function takes an element of `xs` and returns
# an integer, which is used as indexes to create a
# multidimensional array that allows for direct access
# of subsets of the original list via the operator `array[ix]`.
#
# The first function is used to create the first level of
# the multidimensional array of output, and so on.
#
# List x .
# List (x -> Int) ->
# List (... (List x)...)
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
    if verbose:
      print "building Dico..."
    self.dico = multigroup(words, [len, wordSum])
    if verbose:
      print "indexing done."

    # set up families:
    if verbose:
      sys.stdout.write("creating families... ")
      sys.stdout.flush()
    for ofSameLen in self.dico:
      if verbose:
        sys.stdout.write("#")
        sys.stdout.flush()
      if ofSameLen != None:
        for i in range(len(ofSameLen)):
          ofSameSum = ofSameLen[i]
          if ofSameSum != None:
            ofSameLen[i] = classify(ofSameSum, sorted)
    
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
    ofSameLen = self.dico[L]
    if ofSameLen == None:
      return []
    
    S = wordSum(word)
    if S >= len(ofSameLen):
      return []
    ofSameSum = ofSameLen[S]
    if ofSameSum == None:
      return []
    
    (signatures, families) = ofSameSum
    sig = sorted(word)
    ix = indexOf_div(sig, signatures)
    if ix == -1:
      return []
    else:
      return families[ix][:]


# ----
# String
dicopath = "dico.txt"

# The one dictionnary, used to get very fast
# access to any word's families of known anagrams.
# Is imported by the other files as global variable.
#
# Dico
DICO = Dico.fromFile(dicopath, verbose = True)