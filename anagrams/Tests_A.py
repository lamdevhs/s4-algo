# = Projet Anagrammes
# [Algorithmique Avancée] [L2 INFO] [2017 2018] [Nathanael Bayard]

# Note: I recommend reading README.pdf first.

# == Partie A -- Tests

from UnitTest import Test
from A import est_anagramme, anagrammes, best

def testingPartA():
  Test(est_anagramme
    ).check(  input = ("FOO", "BAR"),
              output = False,
              testName = "not anagrams"
    ).check(  input = ("ETFROMAGE", "MEGAFORTE"),
              output = True,
              testName = "are anagrams"
    ).printResults()

  anagrammes_ = lambda word, n: len(anagrammes(word)) == n
  # ^ testing the length of results of anagrammes()
  anagrammes_.__name__ = "anagrammes" # for printing's sake
  Test(anagrammes_
    ).check(  input = ["RUSE", 6],
              output = True,
              testName = "family of 'RUSE'"
    ).check(  input = ["TSAR", 6],
              output = True,
              testName = "family of 'TSAR'"
    ).check(  input = ["SALI", 6],
              output = True,
              testName = "family of 'SALI'"
    ).check(  input = ["AIR", 4],
              output = True,
              testName = "family of 'AIR'"
    ).printResults()

  best_ = lambda L: (len(best(L)[1]), best(L)[0])
  best_.__name__ = "best" # for printing's sake
  Test(best_
    ).check(  input = [2], # L = 2
              output = (15, 2), # 15 families of 2 anagrams
              testName = "family of words of length 2"
    ).check(  input = [3],
              output = (1, 4), # 1 family of 4 anagrams
              testName = "family of words of length 3"
    ).check(  input = [4],
              output = (3, 6), # 3 families of 6 anagrams
              testName = "family of words of length 4"
    ).printResults()


if __name__ == "__main__":
  testingPartA()