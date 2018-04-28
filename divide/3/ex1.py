from random import *


def partition(start, end, L):
	print L, start, end
	pivot = L[end]
	pivotIx = end
	i = start
	j = end - 1
	stuck = False
	while i < j:
		while L[i] < pivot and i < j:
			i += 1
		if i > j:
			L[i], L[pivot] = L[pivot], L[i]
			pivotIx = i
			break

		while L[j] >= pivot and i < j:
			j -= 1
		if i > j:
			L[j+1], L[pivot] = L[pivot], L[j+1]
			pivotIx = j+1
			break

		L[i], L[j] = L[j], L[i]
		i+=1 ; j+=1
		a = L[i]
		
		if i > j:
			L[i], L[pivot] = L[pivot], L[i]
			pivotIx = i
			break
	return (pivotIx, L)

def partition1(start, end, L):
	#print L, start, end
	pivot = L[end]
	i = start
	j = end - 1
	stuck = False
	while i < j:
		a = L[i]
		b = L[j]
		if b <= pivot and a <= pivot:
			i+=1
		elif b > pivot and b > pivot:
			j-=1
		else: #one is before pivot, one is after
			if b <= pivot and a > pivot:
				L[i], L[j] = L[j], L[i]
			i+=1 ; j-=1
	if L[i] > pivot:
		L[i], L[end] = L[end], L[i]
		pivotIx = i
	else:
		L[j+1], L[end] = L[end], L[j+1]
		pivotIx = j+1
	return (pivotIx, L)


def partition2(start, end, L):
	pivot = L[end]
	left = [] ; right = []
	for i in range(start, end):
		if L[i] > pivot:
			right.append(L[i])
		else:
			left.append(L[i])
	before = L[:start]
	return (len(left) + len(before), 
		before
		+ left
		+ [pivot]
		+ right
		+ L[end + 1:]
		)

def quicksort(partitionner, L, inf, sup):
	if inf >= sup:
		return L
	pivotIx, L = partitionner(inf, sup, L)
	L = quicksort(partitionner, L, inf, pivotIx - 1)
	L = quicksort(partitionner, L, pivotIx + 1, sup)
	return L

def tester(verbose = False):
	print "testing..."
	allOk = True
	for i in range(100):
		size = randrange(0, 30)
		L = [randrange(-10,10) for p in range(0, size)]
		expected = sorted(L[:])
		ans1 = quicksort(partition1, L[:], 0, len(L) - 1)
		ans2 = quicksort(partition2, L[:], 0, len(L) - 1)
		if ans1 != ans2 or ans1 != expected:
			allOk = False
			print "---------------------"
			print "houston, we have a problem!"
			print "L =", L
			print "expected =", expected
			print "ans1, ans2 =", ans1, ans2
		elif verbose:
			print "ok:", L
	if allOk:
		print "allOk"

tester(False)