def find_inflection(h):
	inf = []
	for i in xrange(1, len(h)-1):
		if (h[i+1] - h[i]) * (h[i] - h[i-1]) < 0:
			inf.append(i)
	return inf

def is_maxdh_possible(N, K, sabs, dh):
	day = 1
	pos = 0
	it = []
	while day <= K and pos < N-1:
		st = pos
		while pos < N and (sabs[pos] - sabs[st]) <= dh:
			pos += 1
		pos -= 1
		it.append(pos-st)
		day += 1
	return pos == N-1, it

def is_maxkm_possible(N, K, sabs, dh, km):
	day = 1
	pos = 0
	it = []
	while day <= K and pos < N-1:
		st = pos
		while pos < N and (sabs[pos] - sabs[st]) <= dh and pos-st <= km:
			pos += 1
		pos -= 1
		it.append(pos-st)
		day += 1
	return pos == N-1, it


def find_min_h(N, K, sabs):
	lo = 0
	hi = int(2**33)
	while lo < hi:
		mid = lo + (hi-lo)/2
		if is_maxdh_possible(N, K, sabs, mid)[0]:
			hi = mid
		else:
			lo = mid+1
	pos, it = is_maxdh_possible(N, K, sabs, lo)
	if not pos:
		print "FAIL height: {}".format(lo)
	return lo, it

def find_min_km(N, K, sabs, dh):
	lo = 1
	hi = N
	while lo < hi:
		mid = lo + (hi-lo)/2
		if is_maxkm_possible(N, K, sabs, dh, mid)[0]:
			hi = mid
		else:
			lo = mid+1
	pos, it = is_maxkm_possible(N, K, sabs, dh, lo)
	if not pos:
		print "FAIL height: {} km: {}".format(dh, lo)
	return lo, it

def solve(N, K, h):
	sabs = [0 for i in xrange(N)]
	for i in xrange(N-1):
		sabs[i+1] = sabs[i] + abs(h[i+1] - h[i])
	#print sabs
	dh, it = find_min_h(N, K, sabs)
	#print dh
	km, it = find_min_km(N, K, sabs, dh)
	#print km, it
	rsabs = [0 for i in xrange(N)]
	for i in xrange(N-1):
		rsabs[i+1] = rsabs[i] + abs(h[N-2-i] - h[N-1-i])
	pos, it = is_maxkm_possible(N, K, rsabs, dh, km)
	it = it[::-1]
	if len(it) < K:
		dif = K - len(it)
		fin = []
		for i in it:
			if i == 1:
				fin.append(1)
			else:
				v = i
				while dif > 0 and v > 1:
					dif -= 1
					v -= 1
					fin.append(1)
				fin.append(v)
		it = fin
	return ' '.join(map(str, it))

C = int(raw_input())
for case in xrange(1, C+1):
	N, K = map(int, raw_input().split())
	h = map(int, raw_input().split())
	print "Case #{}: {}".format(case, solve(N, K, h))