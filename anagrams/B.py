


# == Partie B

from Tools import classify, identity, indexOf, indexOf_div, nDuplicates
from Dico import (DICO, wordSum)

# === est_presque_anagramme()

# String . String . Int -> Bool
def est_presque_anagramme(a, b, n):
  aL = len(a)
  bL = len(b)
  if len(a) > len(b):
    a, b, aL, bL = b, a, bL, aL

  # now, a <= b
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

# Backtracking algorithm. lastChoice is used to
# force the additional letters to be chosen in
# ascending order, to avoid duplicates.
#
# String . Int -> List String
def presque_anagrammes(word, n, lastChoice = 0, result = None):
  if result == None: # first call
    result = [] # this array is common to the whole stack of calls
  if n == 0:
    result += DICO.anagramsOf(word)
    return result
  else:
    # `lastChoice` forces the chosen letters to be in
    # ascending order, to avoid getting duplicates, since
    # word + ABA = word + BAA = word + AAB
    for choice in range(lastChoice, len(alphabet)):
      letter = alphabet[choice]
      presque_anagrammes(word + letter, n - 1, choice, result)
    return result


#
# Int . Int -> (Int, List Family)
def bestNearOfLength(L, N):
  if len(DICO.dico) <= L or L < 0:
    return (0, [])

  ofSameLen = DICO.dico[L]
  # ^ `ofSameLen` contains all the families of the
  # words of length `L` -- cf Dico.py, or README

  if ofSameLen == None:
    # ^ no families for this length
    return (0, [])

  maxSize = 0
  bestFamilies = []
  for ofSameSum in ofSameLen:
    # ofSameSum: contains families with same `wordSum`
    # cf Dico.py, README
    if ofSameSum != None:
      (signatures, families) = ofSameSum
      for family in families:
        spokesword = family[0]
          # ^ we pick one word as representative
          # of the family
        nearFamily = presque_anagrammes(spokesword, N)
          # ^ we get all the words nearly of the same family
        size = len(nearFamily)
        if size > maxSize:
          maxSize = size
          bestFamilies = [family[:]]
        elif size == maxSize:
          bestFamilies.append(family[:])
  return (maxSize, bestFamilies)


if __name__ == "__main__":
  print "-"*20
  print "Partie B - Questions"
  print "Combien de (familles de) mots possedent\
 un nombre maximal de presque_anagrammes (pour N = 1) ?"
  allResults = []
  for L in range(len(DICO.dico)):
    res = bestNearOfLength(L, 1)
    allResults.append(res)
    print "- pour les mots de longueur", L, ":"
    print "   ", len(res[1]), "famille(s) ayant",
    print res[0], "presque-anagrammes."

  print
  print "Resultat global maximal :"
  globalMax = 0
  globalSolution = []
  for res in allResults:
    (size, families) = res
    if size > globalMax:
      globalMax = size
      globalSolution = [ families ]
    elif size == globalMax:
      globalSolution += families
  print "   ", len(globalSolution), "famille(s) ont",
  print globalMax, "presque-anagrammes."

  print "Ces familles ont-elles des mots tous de meme taille ?"
  sameLen = True
  firstLen = len(globalSolution[0][0])
  for family in globalSolution:
    if len(family[0]) != firstLen:
      sameLen = False
      break
  print "Oui !" if sameLen else "Non !"
