from copy import deepcopy
from random import randrange

# triplets de hoare

# Input: t, N = len(t), a, b, c
# PE:
#   N >= 1
#   (t[a:b+1], <=)
#   (t[b+1:c+1], <=)
# fusion(t, a, b, c)
# PS:
#   (t[a:c+1], <=)
#   t = permut(T)

def fusion(t, a, b, c):
  before = t[0:a]
  after = t[c+1:]
  
  first = t[a : b+1]
  lenF = len(first)
  second = t[b+1 : c+1]
  lenS = len(second)
  aux = []

  i = 0
  j = 0
  

  # inv:
  # note: first/second aren't mutated
  # i <= lenF = b + 1 - a
  # j <= lenS = c + 1 - (b + 1)
  # union(aux, first[i:], second[j:]) = permut(FIRST union SECOND)
  # len(aux) = i + j
  # (aux, <=)

  # variant:
  # v = lenF + lenS - len(aux) = lenF + lenS - (i + j)
  # v = 0 --> not CC

  while lenF + lenS > i + j:
    if j == lenS: # but i != lenF bc CC
      aux.append(first[i])
      i += 1
    elif i == lenF: # but j != lenS bc CC
      aux.append(second[j])
      j += 1

    else:
      a = first[i]
      b = second[j]
      if a <= b:
        aux.append(a)
        i += 1
      else:
        aux.append(b)
        j += 1

  return before + aux + after

def check_fusion(T, t, a, c):
  ref = T[0:a] + sorted(T[a:c+1]) + T[c+1:]
  return t == ref # check no data was lost + functional

def test_fusion(fusionner):
  pb = False
  for i in range(1000):
    size = randrange(1, 20)
    T = [randrange(21) - 10 for p in range(size)]
    #t = deepcopy(T)
    a = randrange(size)
    b = randrange(a, size)
    c = randrange(b, size)
    T = T[0:a] + sorted(T[a:b+1]) + sorted(T[b+1 : c+1]) + T[c+1:]
    t = fusionner(T, a, b, c)
    if not check_fusion(T, t, a, c):
      pb = True
      print "Houston, we have a problem!"
      print "original", T
      print "result", t
      print "args", a, b, c
    else:
      print "ok", T, t, a, b, c
  if not pb:
    print 'all ok'

test_fusion(fusion)