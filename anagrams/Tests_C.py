




# == Partie C -- Tests

from UnitTest import Test, assertion
from C3 import multiAnagrams, A1, A2

def testingPartC():
  count_A1 = lambda word: len(A1(word))
  count_A1.func_name = "count_results_of_A1"
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
  count_A2.func_name = "count_results_of_A2"
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

  # aioli : List String
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

          # def dup(l):
          #   r = []
          #   for i in range(len(l)):
          #     for j in range(i + 1, len(l)):
          #       if l[i] == l[j]:
          #         r.append(l[i])
          #   return r

          # def testvalid(D, string, n):
          #   print "test", string, n
          #   res = multiAnagrams(string, n)
          #   #print res
          #   flat = flatten(res)
          #   print "dup?", len(dup(flat))
          #   print "reslen=", len(flat)
          #   linesToFile(flat, "A" + string + str(n) + ".tempo")

          # def main2():
          #   D = DICO
          #   #testvalid(D, "CHAMPOLLION", 2)
          #   testvalid(D, "AIRAIR", 2)
          #   testvalid(D, "CHAMPOLLION", 4)
          #   #testvalid(D, "CHAMPOLLION", 1)
          #   testvalid(D, "CHAMPOLLION", 3)
          #   #testvalid(D, "CHAMPOLION", 4)

          # if __name__ == "__main__":
          #   for word in ["ROSE", "PROSE", "CHAMPOLLION"]:
          #     res = A1(word)
          #     print word, len(res)

          #   for n in range(1, 6):
          #     res = A2("CHAMPOLLION", n)
          #     print n, len(res)
          #   for i in range(10):
          #     print len(A2("CAROLINEETFLORIAN", i))


