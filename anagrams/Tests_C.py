# = Projet Anagrammes
# [Algorithmique Avancée] [L2 INFO] [2017 2018] [Nathanael Bayard]

# Note: I recommend reading README.pdf first.

# == Partie C -- Tests

from UnitTest import Test, assertion
from C import multiAnagrams, A1, A2
from List import map

def testingPartC():
  count_A1 = lambda word: len(A1(word))
  count_A1.__name__ = "count_results_of_A1"
  Test(count_A1
    ).check(  input = ("ETFROMAGE",),
              output = 192,
              testName = "ETFROMAGE"
    ).check(  input = ("SOURIS",),
              output = 32,
              testName = "SOURIS"
    ).check(  input = ("CHAMPOLLION",),
              output = 599,
              testName = "CHAMPOLLION"
    ).check(  input = ("ROSE",),
              output = 8,
              testName = "ROSE"
    ).check(  input = ("PROSE",),
              output = 11,
              testName = "PROSE"
    ).printResults()

  count_A2 = lambda word, n: len(A2(word, n))
  count_A2.__name__ = "count_results_of_A2"
  Test(count_A2
    ).check(  input = ("CHAMPOLLION", 1),
              output = 0,
              testName = "CHAMPOLLION 1"
    ).check(  input = ("CHAMPOLLION", 2),
              output = 11,
              testName = "CHAMPOLLION 2"
    ).check(  input = ("CHAMPOLLION", 3),
              output = 261,
              testName = "CHAMPOLLION 3"
    ).check(  input = ("CHAMPOLLION", 4),
              output = 599,
              testName = "CHAMPOLLION 4"
    ).check(  input = ("CAROLINEETFLORIAN", 2),
              output = 445,
              testName = "AIOLI CONFRATERNEL"
    ).printResults()

  # List (List String) -> List String
  def toListOfString(xs):
    return map(lambda L: " ".join(L), xs)

  aioli = toListOfString(A2("CAROLINEETFLORIAN", 2))
  assertion('A2(CAROLINEETFLORIAN,2)',
    "AIOLI CONFRATERNEL" in aioli and
    "FINALE CORRELATION" in aioli)

  champo = toListOfString(A1("CHAMPOLLION"))
  assertion('A1(CHAMPOLLION)',
    "MOLLI CHAPON" in champo and
    "PICON MOLLAH" in champo and
    "OH CLIM LAPON" in champo and
    "LOCH LAMPION" in champo)

  cheese = toListOfString(A1("ETFROMAGE"))
  assertion('A1(ETFROMAGE)',
    "MEGA FORTE" in cheese and
    "ME RE GO FAT" in cheese and
    "ET GO FERMA" in cheese)

if __name__ == "__main__":
  testingPartC()