from random import *

# -----------------------------



def fusion_iter(A, B):
	lA = len(A)
	lB = len(B)
	L = []
	a = 0
	b = 0
	while a != lA or b != lB:
		if a == lA:
			L.append(B[b])
			b += 1
		elif b == lB:
			L.append(A[a])
			a += 1
		else:
			xa = A[a]
			xb = B[b]
			if xa < xb:
				L.append(xa)
				a += 1
			else:
				L.append(xb)
				b += 1
	return L

def fusion_recur(A, B):
	if len(A) == 0:
		return B
	elif len(B) == 0:
		return A
	else:
		a, b = A[0], B[0]
		if a < b:
			return [a] + fusion_recur(A[1:], B)
		else:
			return [b] + fusion_recur(A, B[1:])

def insertAfter(L, x, min):
	return L[:min + 1] + [x] + L[min + 1:]

def insert(x, L):
	min = 0
	max = len(L)
	while min < max - 1:
		i = (min + max) // 2
		if L[i] == x:
			return insertAfter(L, x, i)
		elif L[i] < x:
			min = i
		else:
			max = i
	if L[min] >= x:
		return insertAfter(L, x, min - 1)
	else:
		return insertAfter(L, x, min)

def fusion_recur2(L, other):
	if len(other) == 0:
		return L
	else:
		x = other[0]
		return fusion_recur2(insert(x, L), other[1:])


# -----------------------------------

def tri_fusion(fusion, L):
	if len(L) <= 1:
		return L
	d = len(L) // 2
	A = L[:d]
	B = L[d:]
	return fusion(tri_fusion(fusion, A), tri_fusion(fusion, B))

def fusionTester(fusion, verbose = False):
	print "testing...", fusion.func_name
	allOk = True
	for i in range(100):
		sizeA = randrange(1, 10)
		sizeB = randrange(1, 10)
		A = sorted([randrange(0,10) for p in range(0, sizeA)])
		B = sorted([randrange(0,10) for p in range(0, sizeB)])
		if verbose:
			print A, B
		expected = sorted(A + B)
		res = fusion(A, B)
		if expected != res:
			allOk = False
			print "### houston, we have a problem!"
			print "A, B =", A, B
			print "expected =", expected
			print "res =", res
	if allOk:
		print "allOk"

def triTester(fusion, verbose = False):
	print "testing...", fusion.func_name
	allOk = True
	for i in range(100):
		size = randrange(1, 10)
		L = [randrange(0,10) for p in range(0, size)]
		if verbose:
			print L
		expected = sorted(L)
		res = tri_fusion(fusion, L)
		if expected != res:
			allOk = False
			print "houston, we have a problem!"
			print "L =", L
			print "expected =", expected
			print "res =", res
		elif verbose:
			print "ok:", L, expected, res
	if allOk:
		print "allOk"

fusionTester(fusion_iter)
triTester(fusion_iter) #, verbose= True)
fusionTester(fusion_recur)
triTester(fusion_recur)
fusionTester(fusion_recur2)
triTester(fusion_recur2)
