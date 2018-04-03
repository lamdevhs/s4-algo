from random import *

def bestMax0(tab):
	maxi = tab[0] + tab[1]
	for i in range(1,len(tab) - 1):
		val = tab[i] + tab[i+1]
		if val > maxi:
			maxi = val
	return maxi

def bestMax1(tab):
	if len(tab) == 3:
		ans = max(tab[0] + tab[1], tab[1] + tab[2])
	elif len(tab) == 2:
		ans = tab[0] + tab[1]
	else:
		cut = len(tab) // 2
		maxL = bestMax1(tab[0:cut])
		maxR = bestMax1(tab[cut:])
		maxM = tab[cut - 1] + tab[cut]
		ans = max(maxL, maxR, maxM)
	#print "----", tab, ans
	return ans

#print bestMax0([-1,9,-3,12,-5,4])
#print bestMax1([-1,9,-3,12,-5,4])

def tester(verbose = False):
	print "testing..."
	allOk = True
	for i in range(100):
		size = randrange(2, 10)
		L = [randrange(-10,10) for p in range(0, size)]
		if verbose:
			print L
		ans0 = bestMax0(L)
		ans1 = bestMax1(L)
		if ans0 != ans1:
			allOk = False
			print "---------------------"
			print "houston, we have a problem!"
			print "L =", L
			print "ans0, ans1 =", ans0, ans1
		elif verbose:
			print "ok:", ans0, ans1
	if allOk:
		print "allOk"

tester(False)

#print bestMax1([-1,-9,5])