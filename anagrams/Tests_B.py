# = Projet Anagrammes
# [Algorithmique Avancée] [L2 INFO] [2017 2018] [Nathanael Bayard]

# Note: I recommend reading README.pdf first.

# == Partie B -- Tests

from Tools import nDuplicates
from UnitTest import Test, assertion
from B import est_presque_anagramme, presque_anagrammes

def testingPartB():
  Test(est_presque_anagramme
    ).check(  input = ("FOO", "FOO", 1),
              output = False,
              testName = 1
    ).check(  input = ("PAR", "DRAP", 1),
              output = True,
              testName = 2
    ).check(  input = ("PAR", "DRAK", 1),
              output = False,
              testName = 3
    ).check(  input = ("PAR", "PAAR", 1),
              output = True,
              testName = 4
    ).check(  input = ("PAR", "DRAPA", 2),
              output = True,
              testName = 5
    ).check(  input = ("PAR", "PR", 1),
              output = True,
              testName = 6
    ).check(  input = ("PAR", "PARZZZZZZZZZZ", 10),
              output = True,
              testName = 7
    ).printResults()

  near_anagrams_of_PAR = [
    'PARA', 'RAPA', 'PARC', 'DRAP',
    'APRE', 'EPAR', 'PARE', 'RAPE',
    'PAIR', 'PARI', 'PRIA', 'RIPA',
    'PRAO', 'PARS', 'RAPS', 'PART',
    'RAPT', 'PARU', 'RUPA']
  # ^ il n'y a en fait que 19 presque anagrammes, et non 20,
  # pour 'PAR'. en effet, la liste du PDF d'instructions
  # contenait 2 fois le mot 'PARI'.
  assertion("presque_anagrammes('PAR', 1)",
    sorted(near_anagrams_of_PAR) ==
    sorted(presque_anagrammes("PAR", 1)))

  print()
  # String . Int -> Bool
  def checkResults_presque_anagrammes(word, n):
    print("checking results for presque_anagrammes"
      + str((word,n)))
    result = presque_anagrammes(word, n)
    ndup = nDuplicates(result)
    print("... number of duplicated results :", ndup)
    nInvalid = 0
    for answer in result:
      if not est_presque_anagramme(word, answer, n):
        nInvalid += 1
    print("... number of invalid results :", nInvalid)
    isOk = (nInvalid, ndup) == (0,0)
    return isOk

  word = "PAR"
  for i in range(1,6):
    isOk = checkResults_presque_anagrammes(word, i)
    print("... all ok:", isOk)
    print()

if __name__ == "__main__":
  testingPartB()