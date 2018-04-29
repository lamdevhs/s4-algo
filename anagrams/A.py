# = ANAGRAMMES - Projet Algorithmique Avancee
# [Nathanael Bayard] [2017 2018]

# Note: I recommend reading README.pdf first.

# == Partie A

# === est_anagramme()

# String . String -> Bool
def est_anagramme(wa, wb):
  return sorted(wa) == sorted(wb)


# === anagrammes()

from Dico import (DICO)

# String -> Family
def anagrammes(word):
  return DICO.anagramsOf(word)


# === best()

# Returns all the families of maximum size
# which all contain words of length `L`.
#
# Int -> (Int, List Family)
def best(L):
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
      (_, families) = ofSameSum
      for family in families:
        size = len(family)
        if size > maxSize:
          maxSize = size
          bestFamilies = [family[:]]
        elif size == maxSize:
          bestFamilies.append(family[:])

  return (maxSize, bestFamilies)

# Returns all the families  of maximum size,
# regardless of the length of the words inside.
#
# Algorithm: gets the results of best() for all
# lengths, then retain those which have maximum size
# among all those results.
#
# Int -> (Int, List Family)
def bestOfAll():
  maxSize = 0
  bestFamilies = []
  limit = len(DICO.dico)
  for L in range(limit):
    (size, families) = best(L)
    if maxSize < size:
      maxSize = size
      bestFamilies = families
    elif maxSize == size:
      bestFamilies += families

  return (maxSize, bestFamilies)

if __name__ == "__main__":
  print "-"*20
  print "Partie A - Questions"
  print "Combien de familles d'anagrammes sont de taille maximale ?"
  (bestSize, bestFamilies) = bestOfAll()
  print "reponse =", len(bestFamilies)
  print "Quelle est cette taille ?"
  print "reponse =", bestSize
  print "Ces familles contiennent-elles toutes des mots d'une meme longueur ?"
  sameLength = True
  firstLength = len(bestFamilies[0][0])
  for family in bestFamilies:
    if len(family[0]) != firstLength:
      sameLength = False
      break
  print "reponse =", sameLength
  print
  print "Familles de plus grande taille :", bestFamilies