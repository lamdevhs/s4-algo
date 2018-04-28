import math

cpt = 0

def power(x, n):
	global cpt
	if n == 0:
		return 1
	if n % 2 == 0:
		v = power(x, n // 2)
		cpt += 1
		return v*v
	else:
		cpt += 1
		return x*power(x, n - 1)

for i in range(2,200000):
	cpt = 0
	power(2, i)
	print i, cpt/math.log(i)

#m(n)/ln(n) in [1,3] donc 