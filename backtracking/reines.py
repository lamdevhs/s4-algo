def printSol(L, N):
	print "/"*N
	print L
	for x in L:
		print '-'*x + '*' + '-'*(N-x-1)


def placer(N, p, L):
	if p == N:
		printSol(L, N)
	else:
		for x in range(N):
			L.append(x)
			if valide(L, p):
				placer(N, p+1, L)
			L.pop()

def valide(L, p):
	v = L[p]
	for i in range(p):
		x = L[i]
		if v == x:
			return False
		if abs(v - x) == abs(i - p):
			return False
	return True

placer(4, 0, [])