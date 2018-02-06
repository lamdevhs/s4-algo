# Ex 2

# M(0): '0'
# M(1): 1
# M(2): 1+1 = 2
# M(3): (1+1+1) = 3
# M(4): (1+1)*(1+1) = 4
# M(5): (1+1+1)*(1+1) = 15
# M(n): max(a + b = n){M(a)*M(b), M(a)+M(b)}

def paren(n):
  M = [0,1]
  for i in range(2, n+1):
    for k in range(i):
      a = i - k
      b = k
      # a + b = i
      