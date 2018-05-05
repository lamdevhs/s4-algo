"""
Author: Nathanael Bayard
Module Name: List
Description: list/string-related tools.
"""

# ==== List constructors

def strReplicate(amount, pattern):
# strReplicate : Int . String -> String
    if amount <= 0:
        return ''
    return pattern + strReplicate(amount - 1, pattern)


# ==== lists of lists

# The python3 map returns an iterator,
# which i don't care for.
#
def map(f, L):
# map : (a -> b) . List a -> List b
    r = []
    for x in L:
        r.append(f(x))
    return r


# akin to `map` but for lists of lists:
# applies the input function to every subelement
# and returns the resulting new list of lists.
def mapLL(f, LL):
# mapLL : (a -> b) . List (List a) -> List (List b)
    return map(lambda line: map(f, line), LL)

# takes a lists of lists, and fuse each sublist
# into one single "flat" list.
def flatten(LL):
# flatten : List (List a) -> List a
    return reduce(lambda line, line2: line + line2, LL, [])

# ==== pretty printing

# e.g.: asLines([4, [], "foo"]) == "4\n[]\nfoo"
def asLines(L):
# asLines : List a -> String
    return "\n".join(map(str, L))

# e.g.: asWords([4, [], "foo"]) == "4 [] foo"
def asWords(L):
# asWords : List a -> String
    return " ".join(map(str, L))

def concatStrings(L):
# concatStrings : List a -> String
    return "".join(map(str, L))

# function to print a list of lists of values
# as an array with constant-sized columns
def toPrettyStringLL(LL):
# toPrettyStringLL : List a -> String
    if LL == []:
        return ""
        
    # i use `toStr` (written below) instead of the built-in
    # `str` because i want to be able to print
    # lists of lists containing functions (cf UnitTest.py)
    # and by default str(f) would write something like
    # '<function f at 0x7f510ce826e0>'
    # which is ugly and verbose
    strLL = mapLL(toStr, LL)
    
    flattened = flatten(strLL) # flattened so i can use max below
    if flattened == []:
        return ""
    
    maxLen = max(map(len, flattened))
    constantWidth = maxLen + 3
    
    # i add some custom padding to each value of strLL
    # so they each have the same constantWidth
    paddedLL = mapLL(lambda string: padded(string, constantWidth), strLL)
   
    # fuse the elements of each sublist
    lines = map(concatStrings, paddedLL)
    
    # fuse the sublists with \n
    return asLines(lines)

# completes a string with space to its left so its length
# matches a desired value
def padded(string, desiredLength):
    paddingSize = desiredLength - len(string)
    if paddingSize <= 0:
        return string
    return strReplicate(paddingSize, " ") + string

def toPrettyString(L):
# toPrettyString : Line a -> String
    return toPrettyStringLL([L])



# all that follows, up to the definition of `toStr`
# is used to check the type of objects

def dummy_func():
    pass
dummy_tuple = (1,2,3) # for some reason python calls "tuple" any n-uple of whichever size `n`
dummy_list = []

listClass = dummy_list.__class__
functionClass = dummy_func.__class__
tupleClass = dummy_tuple.__class__

# toStr : a -> String
def toStr(x):
    # recursively uses `funcToStr` to replace
    # functions with their __name__ attribute
    # (which is a string) then use the built-in
    # `str` over the result as per usual.
    return str(funcToStr(x))

# this function's type is vaguely complex, since it literally
# depends on its input values (aka it pertains to type dependency)
def funcToStr(x):
    if x.__class__ == functionClass:
        return "<" + x.func_name + ">"
    elif x.__class__ == listClass or x.__class__ == tupleClass:
        return map(funcToStr, x)
    else:
        return x
