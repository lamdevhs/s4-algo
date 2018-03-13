from copy import deepcopy

# Ex 7
def q1():
	m = [[0,1],[10,11]]
	mc = m[:]
	mc[0][0] = 4
	print m, mc

q1()

def q2():
	m = [[0,1],[10,11]]
	mc = deepcopy(m)
	mc[0][0] = 4
	print m, mc
q2()

def q3():
	L0 = [0,1]
	L1 = [10,11]
	m = [L0,L1]
	mc = [L0[:],L1[:]]
	mc[0][0] = 4