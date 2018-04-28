import math

def dicho2(f, A, B, epsi):
	if f(B)*f(A) >= 0:
		raise Exception(f(B)*f(A))
	a = A
	b = B
	while b - a >= epsi:
		c = (b + a)/2.0
		if f(c)*f(b) > 0:
			# f(c) same sign than f(b)
			b = c
		else:
			a = c
	return (b + a)/2


print "sqrt 2 =", dicho2(lambda x: x**2 - 2, 0.0, 3.0, 0.00001)
print "e =", dicho2(lambda x: math.log(x) - 1, 1.0, 3.0, 0.00001)
print "pi =", 2*dicho2(lambda x: math.cos(x), 1.0, 3.0, 0.000001)