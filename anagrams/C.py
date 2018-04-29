
from copy import copy
from Tools import (linesToFile, identity, classify)
from Dico import (Dico, DICO)



def rebuildString(letters, amounts):
  r = ""
  for i in range(len(letters)):
    r += letters[i]*amounts[i]
  return r

# == Partie C

# === multiAnagrams() -- function used by A1() and A2()

# The backtracking to get all the multiAnagrams()
# of a word is so horrendously complicated that
# I decided to create a class just to handle
# all the necessary parameters, to avoid having
# a function which takes 11 arguments.
class BTState():
  def __init__(self,
    result,
    nWordsLeft,
    letters,
    amountsLeft,
    nLettersLeft,

    minNextLen = 1,
    nextWordLen = None,
    selection = "",
    prevSelection = None,
    nextLetter = 0,
    partial = []    ): # so sad...
    # -----------------------------
    self.result = result
    self.nWordsLeft = nWordsLeft
    self.letters = letters
    self.amountsLeft = amountsLeft
    self.nLettersLeft = nLettersLeft

    self.minNextLen = minNextLen
    self.nextWordLen = nextWordLen
    self.selection = selection
    self.prevSelection = prevSelection
    self.nextLetter = nextLetter
    self.partial = partial   


# The motor of A1() and A2().
# Returns the list of lists of families
# such that, by picking one word in each
# family of any of those lists, we'd get
# a multi-anagram of inputString.
# E.G.:
#    'ALETR' ->
#    [  [ ['LE'], ['ART', 'RAT', 'TAR'] ],
#       [ ['RA'], ['LET', 'TEL'] ],
#       [ ['LA'], ['TER'] ]
#    ]
# because
#    LE + any in {ART, RAT, TAR} ~= ALETR
#    RA + any in {LET, TEL} ~= ALETR
#    LA + TER ~= ALETR
#
# String . Int ->
# List (List Family)
def multiAnagrams(inputString, numberOfWords):
  result = []
  inputString = sorted(inputString)
  (letters, grouped) = classify(inputString, identity)

  S = BTState(
    result = result,
    nWordsLeft = numberOfWords,
    letters = letters,
    amountsLeft = map(len, grouped),
    nLettersLeft = len(inputString))

  multiAnagrams_backtracker(S)
  return result

# The very delicate and complicated backtracker that
# gets the results for multiAnagrams().
# Its unique input is of type BTState, and contains
# all the 11 parameters needed to make it work. These
# are as follows:
#
#   S.result : List (List Family)
#       contains the result of the whole process.
#   S.nWordsLeft : Int
#       number of words/families left to find
#       at any given time.
#   S.letters : List Char
#       list of available letters in the "pool",
#       without multiplicity. this array does not change
#       during the whole process.
#   S.amountsLeft : List Int
#       list of amounts left to choose from for each letter
#       in S.letters, at any given time.
#   S.nLettersLeft : Int
#       number of letters left (with multiplicity).
#       is always equal to sum(S.amountsLeft).
#   S.minNextLen : Int
#       the words must be in ascending order of length
#       so this is the lower limit for the next word's
#       length to choose.
#   S.nextWordLen : Int
#       current/next word's length, chosen previously,
#       unless it equals None.
#   S.selection : String
#       the selection of letters (with multiplicity)
#       which will be used to find the next family,
#       once len(S.selection) == S.nextWordLen
#   S.prevSelection : String
#       families must be in ascending order of signatures,
#       to avoid duplicates, so this is the selection of
#       the previous word/family found.
#   S.nextLetter : Int
#       index of the next letter to choose the quantity of,
#       relative to the array S.letters of course.
#   S.partial : List Family
#       one of the solutions, in construction along the way;
#       is appended to S.result once it is completed.
#
# BTState -> Void
def multiAnagrams_backtracker(S):
  if S.nWordsLeft == 0:
    return

  elif S.nWordsLeft == 1:
    # one word/family left to find
    # so we must use all the remaining letters
    # in all the amounts that are left
    S.selection = rebuildString(S.letters, S.amountsLeft)
    selLen = len(S.selection)
    if (S.prevSelection != None and
      selLen == len(S.prevSelection) and
      S.selection < S.prevSelection):
      return
      # deadend: to avoid duplicates,
      # we force the families/words to be in
      # either ascending order of wordlength
      # or in ascending order alphabetically

    anagrams = DICO.anagramsOf(S.selection)
    if len(anagrams) != 0:
      S.result.append(S.partial + [anagrams])

  else:
    # more than one word/family left to find
    if S.nextWordLen == None:
      # no length of word was decided yet
      minL = S.minNextLen
      maxL = S.nLettersLeft // S.nWordsLeft
      # since words are in ascending order
      # of lengths, the next word must have
      # at least the length of the previous word,
      # and must be maximum of length maxL, such
      # that maxL * S.nWordsLeft <= S.nLettersLeft
      # otherwise there wouldn't be enough letters
      # left for all the next remaining words.
      for L in range(minL, 1 + maxL):
        newS = copy(S)
        newS.nextWordLen = L
        newS.selection = ""
        newS.nextLetter = 0
        multiAnagrams_backtracker(newS)

    else:
      # we decided on a length for the current word
      selLen = len(S.selection)
      if selLen == S.nextWordLen:
        # we finished getting all the letters for
        # the current word, aka we reached the length
        # which was decided upon.
        if (S.prevSelection != None and
          selLen == len(S.prevSelection) and
          S.selection < S.prevSelection):
          return
          # deadend (same reason as above)

        anagrams = DICO.anagramsOf(S.selection)
        if len(anagrams) != 0:
          # we add the word/family we found, then we
          # move on to the next word/family.
          newS = copy(S)
          newS.nWordsLeft -= 1
          newS.minNextLen = selLen
          newS.prevSelection = S.selection
          newS.nextWordLen = None
          newS.partial = (S.partial + [anagrams])
          multiAnagrams_backtracker(newS)
      else:
        # we haven't finished selecting the letters
        # of the current word
        if S.nextLetter >= len(S.letters):
          return
          # deadend: we have no more letters to
          # choose from, yet we haven't filled the
          # full length of the current word.

        letter = S.letters[S.nextLetter]
        amountLeft = S.amountsLeft[S.nextLetter]
        maxQ = min(S.nextWordLen - selLen, amountLeft)
        # we can add of any letter up to the minimum
        # of what remains to fill the chosen length of the
        # current word, and of the amount left for
        # that letter in our "pool" of letters.
        for quantity in range(0, maxQ + 1):
          # we choose a particular quantity for the
          # letter, then we move on deeper into the
          # rabbit hole...
          S.amountsLeft[S.nextLetter] -= quantity
          newS = copy(S)
          newS.selection = (S.selection
            + quantity*letter)
          newS.nLettersLeft -= quantity
          newS.nextLetter += 1
          multiAnagrams_backtracker(newS)
          S.amountsLeft[S.nextLetter] += quantity
          # ^ S and newS share the same array `S.amountsLeft`
          # so we have to reset its values after backtracking


# Takes a list of families. Returns the list
# of all (unordered) lists of words that you can form
# by picking one word from each family,
# without duplicates.
# E.G. :
#   [[AB, BA], [AB, BA], [FOO]] ->
#   [[AB, AB, FOO], [AB, BA, FOO], [BA, BA, FOO]]
# Backtracking strategy.
#
# List Family ->
# List (List String)
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


# Takes the output of multiAnagrams()
# and returns the expected output of A1()
# and A2(), aka, a list of list of strings.
# EG:
#   flatten(multiAnagrams("ALETR")) ->
#   [ ['LE', 'ART'],
#     ['LE', 'RAT'],
#     ['LE', 'TAR'],
#     ['RA', 'LET'],
#     ['RA', 'TEL'],
#     ['LA', 'TER']]
#
#
# List (List Family) ->
# List (List String)
def flatten(res):
  r = []
  for sol in res:
    r += multiplyFamilies(sol)
  return r



# === A1() -- at last!

# String ->
# List (List String)
def A1(letters):
  N = len(letters)
  r = []
  for numberOfWords in range(1, N + 1):
    # ^ there's maximum N words of one letter
    # to hope for (i said hope, not expect)
    r += flatten(multiAnagrams(letters, numberOfWords))
  return r


# === A2()

# String . Int ->
# List (List String)
def A2(letters, N):
  r = []
  for numberOfWords in range(1, N + 1):
    r += flatten(multiAnagrams(letters, numberOfWords))
  return r


if __name__ == "__main__":
  for word in ["ROSE", "PROSE", "CHAMPOLLION"]:
    res = A1(word)
    print word, len(res)

  for n in range(1, 6):
    res = A2("CHAMPOLLION", n)
    print n, len(res)
  for i in range(10):
    print len(A2("CAROLINEETFLORIAN", i))
