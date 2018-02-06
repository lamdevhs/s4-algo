# Ex 1

# Sol(1) = 0
# Sol(2) = 2
# Sol(3) = 3 + 2 = 5
# Sol(4) = 4 + 2 + 2 = 8
# Sol(5) = 5 + 3 + 2 + 2 = 5 + Sol(3) + Sol(2)
# Sol(n) = min(j){n + sol(i) + sol(n-j)}


def sol(n):
  L = [0, 0]
  for i in range(2, n + 1):
    minSum = L[1] + L[i - 1]
    for j in range(2, i):
      minSumHere = L[j] + L[i - j]
      if minSumHere < minSum:
        minSum = minSumHere
    L.append(i + minSum)
  return L[n]

for i in range(101):
  print sol(i)
