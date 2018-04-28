


# == Partie B

from Tools import classify, identity, indexOf, indexOf_div, nDuplicates
from Dico import (DICO, wordSum)

# === est_presque_anagramme()

# Smarter version.
#
# String . String . Int -> Bool
def est_presque_anagramme(a, b, n):
  aL = len(a)
  bL = len(b)
  if len(a) > len(b):
    a, b, aL, bL = b, a, bL, aL
  # a <= b
  b = sorted(b)

  if aL + n != bL:
    return False

  (letters_a, amounts_a) = classify(a, identity)
  (letters_b, amounts_b) = classify(b, identity)

  # we check that all the letters in `a` are
  # also in `b`, in the same amount or more
  for letterIx_a in range(len(letters_a)):
    letter = letters_a[letterIx_a]
    letterIx_b = indexOf(letter, letters_b)

    if letterIx_b == -1:
      # ^ `a` contains a letter that b doesn't have
      return False

    if amounts_b[letterIx_b] < amounts_a[letterIx_a]:
      # ^ `a` contains strictly more of some letter than
      # `b` does
      return False

  return True
  # ^ since aL + n == bL,
  # b contains all of the letters of `a` in the same
  # amount, and contains exactly n additional letters


# === presque_anagrammes()

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# String . Int -> List String
def presque_anagrammes(word, n, lastChoice = 0, r = None):
  if r == None: # first call
    r = [] # this array is common to the whole stack of calls
  if n == 0:
    r += DICO.anagramsOf(word)
    return r
  else:
    # `lastChoice` forces the chosen letters to be in
    # ascending order, to avoid getting duplicates, since
    # ABA = BAA = AAB
    for choice in range(lastChoice, 26):
      letter = alphabet[choice]
      presque_anagrammes(word + letter, n - 1, choice, r)
    return r

# Works in theory, but way too slow
#
# Int . Int -> (Int, List Family)
def bestNearOfLength_naive(L, N):
  if len(DICO.dico) <= L or L < 0:
    return (0, [])

  subdico = DICO.dico[L]
  # ^ `subdico` contains all the families of the
  # words of length `L` -- cf Dico.py, or README

  if subdico == None:
    # ^ no families for this length
    return (0, [])

  bestSize = 0
  #bestFamilies = []
  for sumGroup in subdico:
    # sumGroup: contains families with same `wordSum`
    # cf Dico.py, README
    if sumGroup != None:
      (_, families) = sumGroup
      for index in range(len(families)):
        family = families[index]
        spokesword = family[0]
          # ^ we pick one word as representative
          # of the family
        nearFamily = presque_anagrammes(spokesword, N)
          # ^ we get all the words nearly of the same family
        size = len(nearFamily)
        if size > bestSize:
          bestSize = size
          #bestFamilies = [(family[:], nearFamily[:])]
        elif size == bestSize:
          pass
          #bestFamilies.append((family[:], nearFamily[:]))
          # ^ we add the family, not the near family of course
  return bestSize #(bestSize, bestFamilies)

# A lightweight version of presque_anagrammes()
# which only cares about how many near anagrams a word has,
# and only for `n = 1`.
#
# String -> Int
def numberOfNearAnagrams(word):
  r = 0
  for letter in alphabet:
    r += len(DICO.anagramsOf(word + letter))
    # r += DICO.nbAnagramsOf(word + letter)
  return r


#
# String -> Int
def fofofo(word):
  L = len(word) + 1
  if L >= len(DICO.dico):
    return 0

  lenGrp = DICO.dico[L]
  if lenGrp == None:
    return 0
  
  result = 0
  for letter in alphabet:
    nword = sorted(word + letter)
    SS = wordSum(nword)
    if SS >= len(lenGrp):
      continue
    sumGrp = lenGrp[SS]
    if sumGrp == None:
      continue
  
    (signatures, families) = sumGrp
    sig = nword
    ix = indexOf_div(sig, signatures)
    if ix == -1:
      continue
    else:
      result += len(families[ix])

  return result


#
# Int . Int -> (Int, List Family)
def bestNearOfLength(L):
  if len(DICO.dico) <= L or L < 0:
    return (0, [])

  subdico = DICO.dico[L]
  # ^ `subdico` contains all the families of the
  # words of length `L` -- cf Dico.py, or README

  if subdico == None:
    # ^ no families for this length
    return (0, [])

  bestSize = 0
  bestFamilies = []
  for sumGroup in subdico:
    # sumGroup: contains families with same `wordSum`
    # cf Dico.py, README
    if sumGroup != None:
      (_, families) = sumGroup
      for index in range(len(families)):
        family = families[index]
        spokesword = family[0]
          # ^ we pick one word as representative
          # of the family
        nearFamilySize = fofofo(spokesword)
          # ^ we get all the words nearly of the same family
        size = nearFamilySize
        if size > bestSize:
          bestSize = size
          bestFamilies = [family[:]]
        elif size == bestSize:
          pass
          bestFamilies.append(family[:])
          # ^ we add the family, not the near family of course
  return (bestSize, bestFamilies)



if __name__ == "__main__":
  print "-"*20
  print "Partie B - Questions"
  print "Combien de (familles de) mots possedent\
 un nombre maximal de presque_anagrammes (pour N = 1) ?"
  print len(presque_anagrammes("SATIRE", 1))
  #exit(0)
  for i in range(16):
    #print bestNearOfLength_naive(i, 1)
    print bestNearOfLength(i)
  exit(0)
  results = map(bestNearOfLength, range(16))
  print "done res"
  maxi = 0
  maxiL = []
  for i in range(16):
    #print results[i]
    if results[i][0] > maxi:
      maxiL = [ results[i][1] ]
      maxi = results[i][0]
    elif results[i][0] == maxi:
      maxiL.append(results[i][1])
  print maxi
  print maxiL
