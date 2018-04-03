from random import *

def seq_iter(v, L):
	for x in L:
		if x == v:
			return True
	return False

def seq_recur(v, L, i = 0):
	if len(L) <= i:
		return False
	if L[i] == v:
		return True
	return seq_recur(v, L, i+1)

#-------------------------------------------

def div_iter(v, L):
	min = 0
	max = len(L)
	while min < max - 1:
		i = (min + max) // 2
		if L[i] == v:
			return True
		elif L[i] < v:
			min = i
		else:
			max = i
	if L[min] == v:
		return True
	else:
		return False


def div_recur(v, L, min = 0, max = -1):
	if max == -1:
		max = len(L)
	if min < max -1:
		i = (min + max) // 2
		if L[i] == v:
			return True
		elif L[i] < v:
			min = i
		else:
			max = i
		return div_recur(v, L, min, max)
	else:
		if L[min] == v:
			return True
		else:
			return False
		



#-------------------------------------------

def tester(finder, verbose = False):
	print "testing...", finder.func_name
	nTimesInList = 0
	allOk = True
	for i in range(100):
		size = randrange(1, 10)
		toFind = randrange(0,10)
		L = [randrange(0,10) for p in range(0, size)]
		if verbose:
			print L, toFind
		L.sort()
		isInList = toFind in L
		if isInList:
			nTimesInList += 1

		res = finder(toFind, L)
		if isInList != res:
			allOk = False
			print "### houston, we have a problem!"
			print "L =", L
			print "toFind =", toFind
			print "isInList =", isInList
			print "res =", res
	if allOk:
		print "allOk",
	if verbose:
		print nTimesInList
	else:
		print

tester(seq_iter)
tester(seq_recur)
tester(div_iter)
tester(div_recur)
