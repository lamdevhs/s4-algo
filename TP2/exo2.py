def holland(t):
  b = 0
  w = 0
  # search for r:
  r = len(t) - 1
  while r >= 0 and t[r] == "red":
    r -= 1
  # if r == -1: # array is full of reds
  #   return t
  # inv:
  # 0 <= b <= w <= r+1 <= len(t)
  # forall k [0, b-1], t[k] = blue
  # forall k [b, w-1], t[k] = white
  # forall k [r-1, N-1], t[k] = red
  # t = premut(T)
  while w <= r:
    if t[w] == "white":
      w += 1
    elif t[w] == "blue":
      # w est bleue,
      # b est blanche
      # on swap et avance 
      t[b], t[w] = t[w], t[b]
      b += 1
      w += 1
    elif t[w] == "red":
      t[w], t[r] = t[r], t[w]
      r -= 1
      # w n'est pas avance

  return t

r = "red"; w = "white"; b = "blue"
t = [r, w, b, w, r, b, w, r, r, w, r, r]
t = [r, r, r, r]
t = [b, b, b, b]
t = [w, w, w, w]
print holland(t)
