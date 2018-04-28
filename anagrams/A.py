# = ANAGRAMMES - Projet Algorithmique Avancee
# [Nathanael Bayard] [2017 2018]

# Note: type "Family" == type "List String"
# *Family* = list of words sharing the same letters
# aka, the *family* of a word is the sets of its anagrams

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
      # for index in range(len(families)):
      #  family = families[index]
      for family in families:
        size = len(family)
        if size > bestSize:
          bestSize = size
          bestFamilies = [family[:]]
        elif size == bestSize:
          bestFamilies.append(family[:])
  return (bestSize, bestFamilies)


# Returns all the families  of maximum size,
# regardless of the length of the words inside.
#
# Algorithm: gets the results of best() for all
# lengths, then retain those which have maximum size.
#
# Int -> (Int, List Family)
def bestOfAll():
  bestSize = 0
  bestFamilies = []
  limit = len(DICO.dico)
  for L in range(limit):
    (size, families) = best(L)
    if bestSize < size:
      bestSize = size
      bestFamilies = families
    elif bestSize == size:
      bestFamilies += families

  return (bestSize, bestFamilies)

if __name__ == "__main__":
  print "-"*20
  print "Partie A - Questions"
  (bestSize, bestFamilies) = bestOfAll()
  print "Combien de familles d'anagrammes sont de taille maximale ?"
  print "reponse =", len(bestFamilies)
  print "Quelle est cette taille ?"
  print "reponse =", bestSize
  print "Ces familles contiennent-elles toutes des mots d'une meme longueur ?"
  sameLength = True
  firstLength = len(bestFamilies[0][0])
  for i in range(len(bestFamilies)):
    family = bestFamilies[i]
    if len(family[0]) != firstLength:
      sameLength = False
      break
  print "reponse =", sameLength
  print
  print "Familles de plus grande taille :", bestFamilies