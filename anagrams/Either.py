"""
Author: Nathanael Bayard
Module Name: Either
Description: type to represent potentially erroneous values, with an error message.
"""


#   type Either e a = Left e | Right a
# /
# Two types of values which can have type `Either e a`:
# /
#   Left(x) : Either e a
#   Right(y) : Either e a
# /
# With `x : e` and `y : a` of course
# By convention, (and as a pun over `Right`) although `Either` symmetrical
# with relation to the types `e` and `a`, we generally use `e`
# for the types of messages of error (nearly always, `e = String`)
# and `a` for the types of values when there's no error.
# `Left(x)` thus represents an error and `x` is a report of that error,
# `Right(y)` represents a successful result with `y` as its actual content.
#
# algebraically speaking, the type `Either e a` represents the union of the 
# types `e` and `a`.
#
# Example of trivial function which could be written with `Either`,
# here with `e = String` and `a = List t` :
# /
#   # head : List t -> Either String (List t)
#   def head(list):
#       if list == []:
#           return Left("can't get the head of an empty list")
#       else:
#           return Right(list[0])
# /
class Either():

    # this constructor is not meant to be called directly.
    # below the Either class are the two proper ways to get
    # a value of type `Either e a`: Left and Right
    def __init__(self, value, isLeft = False):
        if isLeft:
            self.leftValue = value
        else:
            self.rightValue = value
        self.isLeft = isLeft
        self.isRight = not isLeft
    
    # cf PDF for more in-depth explanation
    # takes the result of a previous operation and either simply transmit
    # the error report, or do something with the content of the successful
    # result, outputting from then on either a new successful result, or an
    # error report of its own.
    # axiomatically:
    # /
    #   Left(x).eitherDo(f, other_args) == Left(x)
    #   Right(y).eitherDo(f, other_args) == f(y, other_args)
    # /
    # with `f(y, other_args) : Either e b`
    # and so esp we can have `f(y, other_args) == Left(z)`
    # aka `f` can fail too.
    #
    # so, putting aside the variadic stuff (only necessary because
    # python does not allow arbitrary currying of functions)
    # /
    #   eitherDo : Either e a . (a -> Either e b) -> Either e b
    def eitherDo(self, f, *args):
        if self.isLeft:
            return self
        else:
            return f(self.rightValue, *args)

    # cf PDF for more in-depth explanation
    # takes a function (a -> b) and `Either` an error report, or a successful
    # result of content of type `a`. `Either` returns the error report as is, or a new
    # successful result being the output of the function applied to the previous
    # result's content.
    #
    # axiomatically:
    # /
    #   Left(x).eitherApply(f, other_args) == Left(x)
    #   Right(x).eitherApply(f, other_args) == Right(f(x, other_args))
    # /
    # with `f(x, other_args)` a function of type `b`
    # so, putting aside the variadic stuff:
    # /
    #   eitherApply : Maybe a . (a -> b) -> Maybe b
    def eitherApply(self, f, *args):
        if self.isLeft:
            return self
        else:
            return Right(f(self.rightValue, *args))

#   Right : a -> Either e a
def Right(value):
    return Either(value, isLeft = False)

#   Left : e -> Either e a
def Left(value):
    return Either(value, isLeft = True)


# maps a function `f` which may fail (return `Left(report)`)
# over a list `xs`. returns the first error report if one call to `f`
# 'fails', returns the result of the mapping (encased in `Right`)
# otherwise.
#
#   eitherMap : (a -> Either e b) . List a -> Either e (List b)
def eitherMap(f, xs):
    out = []
    for x in xs:
        y = f(x)
        if y.isLeft: # if y == Left(report)
            return y
        else:
            out.append(y.rightValue)
    return Right(out)
