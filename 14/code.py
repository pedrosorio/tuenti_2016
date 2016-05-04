#Summary:
#The naive approach is to do a BFS using "set of keys collected" + "current position" as the state
#However that would take N * M * 2^K ~ 300^2 * 2^16 ~ 5.8 * 10^9
#Instead what I do is to do a BFS from every point to every other point (Start, keys, End)
#Once I have the minimum command list (according to the statement) to go from every point A to B
#I use DP (https://en.wikipedia.org/wiki/Held%E2%80%93Karp_algorithm) to determine the optimal
#way to go from S -> collect all keys -> E
#This solution becomes N * M * (K+2)^2 (BFS) + (K+1)^2 * 2^(K+1) ~ 300 * 300 * 18^2 + 17^2 * 2^17 ~ 6.7 * 10^7 (100 times faster :D)
#There may be another factor of 10 here because I am iterating over a ~16 bit number to get the set bits, and it's not terribly optimized
#Also, the code is ugly including some bad repetition in the BFS that could be removed
#Still.. Python is SLOWWWW.... 15 minutes to run the submit phase...

from collections import deque

def get_1_bits(n):
	return [i for i in xrange(1, 18) if n & (1<<i)]

def add_mvs_to_num(mvs_str, num):
	for mv in mvs_str:
		num *= 4
		if mv == 'D':
			num += 1
		elif mv == 'S':
			num += 2
		elif mv == 'W':
			num += 3
	return num 

def compute_D(D, p, S, c, mvs):
	if (S, c) in D:
		return D[(S, c)]
	Smc = S - (1<<c)
	#print S, Smc, c
	bits = get_1_bits(Smc)
	dst_min, mv_num_min, mv_ct_min, pre_x = 100000000000000, 0, 0, -1 
	for x in bits:
		dst, mv_num, mv_ct = compute_D(D, p, Smc, x, mvs)
		if mvs[x][c] is None:
			continue
		this_dst = dst + mvs[x][c][0]
		if this_dst <= dst_min:
			this_mv_num = add_mvs_to_num(mvs[x][c][1], mv_num)
			this_mv_ct = mv_ct + len(mvs[x][c][1])
			if this_dst == dst_min:
				if this_mv_ct > mv_ct_min:
					continue
				if this_mv_ct == mv_ct_min and this_mv_num > mv_num_min:
					continue 
			dst_min = this_dst
			mv_num_min = this_mv_num
			mv_ct_min = this_mv_ct
			pre_x = x
	D[(S,c)] = (dst_min, mv_num_min, mv_ct_min)
	p[(S,c)] = pre_x
	return D[(S, c)]

# Solves a dp to get from start to exit going through all keys
# mvs is a matrix where mvs[i][j] is a tuple (#moves, move_string) with optimal moves to go from point i to point j
# move_string is included to find the smallest lexycographic path if several with same length are available
# i = 0 -> starting
# i = 1:len(mvs)-1 -> keys
# i = len(mvs)-1 -> exit
def tsp(mvs, PRINT):
	D = {}
	p = {}
	for c in xrange(1, len(mvs)):
		S = 1 << c
		if mvs[0][c] is None:
			D[(S, c)] = 1000000000000, 0, 0
		else:
			D[(S, c)] = mvs[0][c][0], add_mvs_to_num(mvs[0][c][1], 0), len(mvs[0][c][1])
		p[(S, c)] = 0
	for S in xrange(3, 1 << len(mvs)):
		if S & 1:
			continue
		for c in get_1_bits(S):
			compute_D(D, p, S, c, mvs)
	S = sum([1<<i for i in xrange(1, len(mvs))])
	#print p
	#print D
	mv_str = ""
	x = len(mvs)-1
	ct = 0
	while x != 0:
		if PRINT:
			print S, x
		if (S, x) not in p:
			return None
		pre_x = p[(S, x)]
		if PRINT:
			print pre_x
		if mvs[pre_x][x] is None or mvs[pre_x][x] == 0:
			return None
		if PRINT:
			print mvs[pre_x][x]
		mv_str = mvs[pre_x][x][1] + mv_str
		ct += mvs[pre_x][x][0]
		S -= 1 << x
		x = pre_x
	return ct, mv_str 

mv_cmds = [('A', 0, -1), ('D', 0, 1), ('S', 1, 0), ('W', -1, 0)]

def bfs(mp, loc0, loc1, PRINT):
	y0,x0 = loc0
	y1,x1 = loc1
	N, M = len(mp), len(mp[0])
	vis = set([(y0, x0)])
	fr = {(y0,x0): ('', (0, 0), 0, 0, 0)}
	q = deque([(y0, x0, 0)])
	sol_it = 10000000000000
	sols = []
	while q:
		y, x, it = q.pop()
		if it > sol_it:
			break
		if (y, x) == (y1, x1):
			sol_it = it
			continue
		if y < N-1 and mp[y+1][x] not in '#H' and mp[y][x] != 'H':
			mv_ct, mv_num = fr[(y, x)][-2:]
			if (y+1, x) in fr:
				c_f, loc_f, it_f, mv_ct_f, mv_num_f = fr[(y+1, x)]
				if it+1 > it_f:
					continue
				if mv_ct > mv_ct_f:
					continue
				if mv_ct == mv_ct_f and mv_num > mv_num_f:
					continue
				fr[(y+1, x)] = ('', (y, x), it+1, mv_ct, mv_num)
				continue
			fr[(y+1, x)] = ('', (y, x), it+1, mv_ct, mv_num)
			q.appendleft((y+1, x, it+1))
			continue
		for ch, dy, dx in mv_cmds:
			# doesn't wrap vertically but there are always walls at the bottom so we're safe
			ny = (y + dy) % N
			nx = (x + dx) % M
			if (ny, nx) not in vis and mp[ny][nx] != '#':
				mv_ct, mv_num = fr[(y, x)][-2:]
				mv_ct += 1
				mv_num = add_mvs_to_num(ch, mv_num)
				if (ny, nx) in fr:
					c_f, loc_f, it_f, mv_ct_f, mv_num_f = fr[(ny, nx)]
					if it+1 > it_f:
						continue
					if mv_ct > mv_ct_f:
						continue
					if mv_ct == mv_ct_f and mv_num > mv_num_f:
						continue
					fr[(ny, nx)] = (ch, (y, x), it+1, mv_ct, mv_num)
					continue
				fr[(ny, nx)] = (ch, (y, x), it+1, mv_ct, mv_num)
				q.appendleft((ny, nx, it+1))
	if (y1, x1) not in fr:
		return None
	ct = 0
	mv_str = ''
	cur = (y1, x1)
	while cur != (y0, x0):
		ch, cur = fr[cur][:2]
		mv_str = ch + mv_str
		ct += 1
	return ct, mv_str
		

def solve(mp, N, M, PRINT):
	key_locs = []
	for i in xrange(N):
		for j in xrange(M):
			if mp[i][j] == 'S':
				yS, xS = i, j
			elif mp[i][j] == 'E':
				yE, xE = i, j
			elif mp[i][j] == 'K':
				key_locs.append((i, j))
	locs = [(yS,xS)] + key_locs + [(yE,xE)]
	mvs = [[0 for j in xrange(len(locs))] for i in xrange(len(locs))]
	for i in xrange(len(locs)):
		for j in xrange(len(locs)):
			if i == j:
				continue
			mvs[i][j] = bfs(mp, locs[i], locs[j], PRINT)
	if PRINT:
		print locs
		print mvs
	res = tsp(mvs, PRINT)
	if PRINT:
		print res
	if res is None:
		return "IMPOSSIBLE"
	else:
		return ' '.join(map(str, res))


T = int(raw_input())
for case in xrange(1,T+1):
	N, M = map(int, raw_input().split())
	mp = [[c for c in raw_input().strip()] for _ in xrange(N)]
	PRINT = False
	if PRINT:
		print '\n'.join([''.join(line) for line in mp])
	print "Case #{}: {}".format(case, solve(mp, N, M, PRINT))
