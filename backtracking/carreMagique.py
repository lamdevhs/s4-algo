def checkAddition(S, L, N, p):
	checkLine(S, L, N, p)
	for j in range(N):
		checkCol(S, L, j, p)
	for k in range(N):
		check()

def checkLine(S, L, N, p):
	line = p // N
	col = p % N
	partLine = L[line*N : p + 1]
	s = sum(partLine)
	if col == N - 1:
		return s == S
	else:
		return s <= S

def checkCol(S, L, N, p):
	line = p // N
	col = p % N
	partCol = [ L[N*k + col]
		for k in range(0,line + 1) ]
	s = sum(partCol)
	if line == N - 1:
		return s == S
	else:
		return s <= S

def checkDiag(S, L, N, p):
	line = p // N
	col = p % N
	res = True
	if line == col: # backslash
		partDiag = [ L[N*k + k]
			for k in range(0, line + 1) ]
		s = sum(partDiag)
		if line == N - 1:
			res = res and s == S
		else:
			res = res and s <= S
	if line + col == N - 1: # slash
		partDiag = [ L[N*k + (N-1-k)]
			for k in range(0, line + 1) ]
		s = sum(partDiag)
		if line == N - 1:
			res = res and s == S
		else:
			res = res and s <= S
	return res

def placer(L, S, p, N):
  if L == None:
  	L = [0]*N*N
  if S == None:
  	S = n * (n*n + 1) / 2
  if N*N == p:
    handle(L, N)
  else:
    for x in D(N):
      # print x
      L.append(x)
      if checkAddition(S, L, N, p):
        placer(L, S, p+1, N)
      L.pop()

def handle(L, N):
  print ","*N
  for i in range(N):
    for k in range(i*N, (i+1)*N):
      x = L[k]
      print x,
      if k % 3 == 2 and k % N != N-1:
        print "|",
    print
    if i % 3 == 2 and i % N != N-1:
      print "-"*21
    

def D(N):
  return range(1, N+1)


N = 3
placer(None, None 0, N)