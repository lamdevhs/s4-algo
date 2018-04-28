
from List import toPrettyStringLL

# basic unit testing strategy for pure fonctions: checks the output
# of a function is consistent with various outputs given.
# also checks if the function throws an error for the right (wrong)
# kind of arguments.
#
# if some checking fails, the inner variable `results` is 
# filled with a row of data containing the name of the failed test,
# the input, the expected output, and the actual output that the
# test obtained from the function tested.
#
# typical usage (cf the unit test modules in `./unitTests`)
# /
# Test(myFunction
#     ).check(input = x, output = y, testName = "test that myFunction(x) == y"
#     ).checkError(input = z, testName = "test that myFunction(z) raises an exception"
#     ).printResults() # <-- print the results to the console.
# /
class Test():
  def __init__(self, functionToTest):
    self.toTest = functionToTest
    self.name = functionToTest.func_name
    self.results = []
  
  #   check : Test (a -> b) . a . b . String -> Void [IO]
  def check(self, input, output, testName = "untitled test"):
    actualOutput = self.toTest(*input)
    if actualOutput != output:
      self.results.append([testName, input, output, actualOutput])
    return self

  #   checkError : Test (a -> b) . a . String -> Void [IO]
  def checkError(self, input, testName = "untitled test"):
    try:
      actualOutput = self.toTest(*input)
      self.results.append([testName, input, "(error)", actualOutput])
    finally:
      return self

  #   printResults : Test (a -> b) . -> Void [IO]
  def printResults(self):
    print 'unit tests for function "' + self.name + '":',
    if len(self.results) == 0:
       print "ok, all tests passed"
    else:
      print len(self.results), "tests failed:"
      report = [["test name",
            "input",
            "expected output",
            "real output"]] + self.results
      print toPrettyStringLL(report)