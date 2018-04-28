
from Tools import (linesToFile, identity, classify)
from Dico import (Dico, DICO)



def rebuildString(letters, amounts):
  r = ""
  for i in range(len(letters)):
    r += letters[i]*amounts[i]
  return r

# Partie C

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
# (END BTState)

# Dico . String ->
# List (List String)
def A1(D, letters):
  r = []
  for L in range(len(D.dico)):
    r += D.multiAnagramsOfLen(letters, L)
  return r

# Dico . String . Int ->
# List (List String)
def multiAnagrams(D, inputString, numberOfWords):
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
  multiAnagrams_backtracker(D, S)
  return solutions

# Dico . BTState -> Void
def multiAnagrams_backtracker(D, S):
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

    anagrams = D.anagramsOf(S.selection)
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
        multiAnagrams_backtracker(D, newS)
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
        anagrams = D.anagramsOf(S.selection)
        if len(anagrams) != 0:
          newS = S.copy()
          newS.nWordsLeft -= 1
          newS.minLenNextWord = S.selLen
          newS.prevWord = S.selection
          newS.nextWordLen = None
          newS.partialSolution = (S.partialSolution
            + [anagrams])
          multiAnagrams_backtracker(D, newS)
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
          multiAnagrams_backtracker(D, newS)
          S.validAmounts[S.nextLetterIx] += quantity
          # ^ S and newS share the same .amounts
          # array, so we have to reset its values
          # after backtracking

          # self.backtracker(NW, NC - quantity, minLen,
          #   letters, amounts,
          #   selection + quantity*letter,
          #   selLen + quantity, Len, whichLetter + 1,
          #   solutions, partialSolution)

# ---------------------------
# ---------------------------
# M A I N


def dup(l):
  r = []
  for i in range(len(l)):
    for j in range(i + 1, len(l)):
      if l[i] == l[j]:
        r.append(l[i])
  return r

# List (List String) ->
# List (String)
def multiplyFamilies(families):
  L = len(families)
  result = []
  multiplyFamilies_BT(families, L, 0, None, [None]*L, result)
  return result

def multiplyFamilies_BT(families, L, familyIx, lastChoice,
  partial, result):
  if familyIx == L:
    result.append(partial[:])
  else:
    current = families[familyIx]
    if familyIx == 0: # first family, no prev
      noLimitations = True
    else:
      prev = families[familyIx - 1]
      noLimitations = (prev[0] != current[0])
        # ^ identical to (current != prev)
    if noLimitations:
      for choice in range(len(current)):
        word = current[choice]
        partial[familyIx] = word
        multiplyFamilies_BT(families, L, familyIx + 1, lastChoice = choice,
          partial = partial, result = result)
        partial[familyIx] = None # not really necessary
    else:
      for choice in range(lastChoice, len(current)):
        word = current[choice]
        partial[familyIx] = word
        multiplyFamilies_BT(families, L, familyIx + 1, lastChoice = choice,
          partial = partial, result = result)
        partial[familyIx] = None # not really necessary





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
    r += multiplyFamilies(sol)
  r = map(sorted, r)
  r = map(lambda a: Join(a, " "), r)
  return r

def testvalid(D, string, n):
  print "test", string, n
  res = multiAnagrams(D, string, n)
  #print res
  flat = flatten(res)
  print "dup?", len(dup(flat))
  print "reslen=", len(flat)
  linesToFile(flat, "A" + string + str(n) + ".tempo")

def main():
  D = DICO
  #testvalid(D, "CHAMPOLLION", 2)
  testvalid(D, "AIRAIR", 2)
  testvalid(D, "CHAMPOLLION", 4)
  #testvalid(D, "CHAMPOLLION", 1)
  testvalid(D, "CHAMPOLLION", 3)
  #testvalid(D, "CHAMPOLION", 4)
main()