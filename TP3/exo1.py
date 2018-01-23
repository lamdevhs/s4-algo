from copy import deepcopy
from random import randrange

def partition(xs, deb, fin):
  pivot = xs[deb]
  left = deb + 1
  right = fin # fin included

  # inv:
  # deb <= left <= right + 1 <= fin + 1
  # forall I, I in [deb,left[ -->  xs[I] <= pivot
  # forall I, I in ]right, fin] --> xs[I] > pivot

  # variant: v = (right - left) + 1
  # v <= 0 --> not CC
  while left <= right:
    if xs[left] <= pivot:
      left += 1
    elif xs[right] > pivot:
      right -= 1
    else:
      # then xs[left] > pivot and xs[right] <= pivot
      # so we swap
      xs[left], xs[right] = xs[right], xs[left]

      # we know left != right bc
      # no value can be both <= pivot and > pivot
      left += 1
      right -= 1

  a = left - 1 # final position of pivot

  # works even if a == deb + 1
  # aka we didn't change left from its initial value
  xs[a], xs[deb] = pivot, xs[a]

  return a

def check_partition(xs, debut, fin, pivotIx):
  v = xs[pivotIx]
  for i in range(debut, pivotIx):
    if xs[i] > v:
      return False
  for j in range(pivotIx + 1, fin):
    if xs[j] <= v:
      return False
  return True

def test_partition(partitionner):
  pb = False
  for i in range(1000):
    size = randrange(1, 20)
    T = [randrange(21) - 10 for p in range(size)]
    t = deepcopy(T)
    debut = randrange(size)
    fin = randrange(debut, size)
    pivotIx = partitionner(t, debut, fin)
    if not check_partition(t, debut, fin, pivotIx):
      pb = True
      print "Houston, we have a problem!"
      print "original", T
      print "result", t
    else:
      print "ok", T, t, debut, fin, pivotIx
  if not pb:
    print 'all ok'

test_partition(partition)