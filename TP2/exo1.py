from copy import deepcopy
from random import randrange

def insertion2(t, k):
  i = k
  e = t[k]
  for j in range(k):
    if t[j] >= e:
      i = j
      break
  return t[:i] + [e] + t[i:k] + t[k+1:]


def PE(N, k, t):
  return (1 < N and 0 < k and k < N
    and t[:k] == sorted(t[:k]))

def inv2(t, T, k, j, x):
  return (0 <= j and j < k
    and x == T[k] and t[j] > x
    and t[j+1:k+1] == T[j:k]
    and t[:j] == T[:j])

def CC(t, j, x):
  return j > 0 and t[j - 1] > x

def PS(t, T, k):
  return sorted(T[:k+1]) == t[:k+1]


def insertion3(t, k):
  N = len(t)
  assert(PE(N, k, t))
  T = t[:]
  if t[k] < t[k - 1]:
    x = T[k]
    j = k - 1
    t[k] = t[k-1]
    assert(inv2(t, T, k, j, x))

    while CC(t, j, x):
      assert(inv2(t, T, k, j, x)
        and CC(t, j, x))
      t[j] = t[j - 1]
      j -= 1
      assert(inv2(t, T, k, j, x))

    assert(inv2(t, T, k, j, x)
      and not CC(t, j, x))
    t[j] = x
  assert(PS(t, T, k))



def tri_insertion(t):
  for i in range(1, len(t)):
    insertion3(t, i)
  return t


# t = [0,-1,45,20,-15,7,129,-8]
# print tri_insertion(t)

def test_tri(sorter):
  pb = False
  for i in range(1000):
    size = randrange(10)
    T = [randrange(21) - 10 for p in range(size)]
    t = deepcopy(T)
    if sorted(T) != sorter(t):
      pb = True
      print "Houston, we have a problem"
      print T
      print t
  if not pb:
    print 'all ok'

test_tri(tri_insertion)




