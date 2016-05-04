# NOTE TO SELF: I should have skipped this problem on Thursday :D
# A mish-mash of "find periods in the sequence of digits at position (i,j)" and 
# Give up and compute the exponential anyway if you don't find a period (which is very convenient as it happens for small N only...)
# Probably wrong answer and I don't see how this could be computed otherwise (keeping track of powers of 2,5 in the numerator to cancel out
# the denominator prevents efficient computation of matrix multiplication which requires sums and there is no way to determine if the sum of
# elements will add up to a power of 2 or 5 if one keeps only the last digit of the numerator). Can't wait to see the solution!
from math import log
import datetime
LOG2, LOG5 = log(2), log(5)
STORED_MATS = {}

def sum_all(nums):
	res = [[0, 0, 0], [2, 2]]
	fin = 0
	mx2, mx5 = max((n[1][0] for n in nums)), max((n[1][1] for n in nums))
	for n in nums:
		if n[0][2] == 0:
			continue
		fin += (2 ** (n[0][0] + mx2 - n[1][0])) * (5 ** (n[0][1] + mx5 - n[1][1])) * n[0][2]
	return red_frac([get_2_5_rest(fin), [mx2, mx5]])

def max_i(nums):
	mx2, mx5 = max((n[1][0] for n in nums)), max((n[1][1] for n in nums))
	mxi = 0
	mxlog = 0
	for i in xrange(0, len(nums)):
		n = nums[i]
		if n[0][2] == 0:
			continue
		vlog = LOG2 * (n[0][0] + mx2 - n[1][0]) + LOG5 * (n[0][1] + mx5 - n[1][1]) + log(n[0][2])
		if vlog >= mxlog:
			mxlog = vlog
			mxi = i
	return mxi

def mul(a, b):
	if a[0][2] == 0 or b[0][2] == 0:
		return [[0, 0, 0], [0, 0]]
	return red_frac([[a[0][0] + b[0][0], a[0][1] + b[0][1], a[0][2] * b[0][2]], [a[1][0] + b[1][0], a[1][1] + b[1][1]]])

def mat_mult(A, B):
	N = len(A)
	return [[sum_all([mul(A[i][k], B[k][j]) for k in xrange(N)]) for j in xrange(N)] for i in xrange(N)]

def mat_exp(A, n):
		N = len(A)
		if n == 1:
			return A
		if n in STORED_MATS:
			return STORED_MATS[n]
		if n-1 in STORED_MATS:
			return mat_mult(STORED_MATS[n-1], A)
		An_2 = mat_exp(A, n/2)
		An = mat_mult(An_2, An_2)
		if n & 1:
			An = mat_mult(An, A)
		return An

def get_mod_10(n2, n5, rest):
	v = 1
	if n2 > 0:
		v *= (2 ** ((n2 - 1)%4 + 1)) % 10
	if n5 > 0:
		v *= 5
	return int((v * rest) % 10)

def get_last_digits(num):
	return get_mod_10(*num[0]), get_mod_10(num[1][0], num[1][1], 1)

def solve(patmx, patdig, permx, probs, I, N):
	pat_len = len(patmx[0])
	if N+1 < pat_len:
		mxc = patmx[I][N-1]
		D, d = patdig[mxc][I][N-1]
	else:
		p = permx[I]
		per = patmx[I][-p:]
		mxc = per[(N - (pat_len - p + 1)) % p]
		p = find_period(patdig[mxc][I])
		if p == -1:
			final = mat_exp(probs, N) 
			STORED_MATS[N] = final
			D, d = get_last_digits(final[mxc][I])
		else:
			per = patdig[mxc][I][-p:]
			D, d = per[(N - (pat_len - p + 1)) % p]
	return "Chair: {} Last digits: {}/{}".format(mxc, D, d)

def get_2_5_rest(n):
	if n == 0:
		return [0, 0, 0]
	n2, n5 = 0, 0
	while n & 1 == 0:
		n >>= 1
		n2 += 1
	while n % 5 == 0:
		n /= 5
		n5 += 1
	return [n2, n5, n]

def red_frac(tot):
	mn2, mn5 = min(tot[0][0], tot[1][0]), min(tot[0][1], tot[1][1])
	for i in xrange(2):
		tot[i][0] -= mn2
		tot[i][1] -= mn5
	return tot

def get_patterns(P):
	N = len(P)
	cur = P
	permx = [[] for c in xrange(N)]
	perdig = [[[] for j in xrange(N)] for i in xrange(N)]
	for _ in xrange(1000):
		for I in xrange(N):
			permx[I].append(max_i([cur[c][I] for c in xrange(C)]))
		for i in xrange(N):
			for j in xrange(N):
				perdig[i][j].append(get_last_digits(cur[i][j]))
		cur = mat_mult(cur, P)
	return permx, perdig

def find_period(seq):
	for p in xrange(1, 51):
		times = 1 + 500/p
		is_per = True
		for i in xrange(1,times):
			if seq[-p:] != seq[-p*(i+1):-p*i]:
				is_per = False
				break
		if is_per:
			return p
	return -1

C = int(raw_input())
P = int(raw_input())
probs = [[([0, 0, 0], [0, 0]) for i in xrange(C)] for j in xrange(C)]
for p in xrange(P):
	O, D, p = map(int, raw_input().split('/')[0].split())
	probs[D][O] = red_frac([get_2_5_rest(p), [2, 2]])
patmx, patdig = get_patterns(probs)
permx = map(find_period, patmx)
Q = int(raw_input())
for case in xrange(1, Q+1):
	I, N = map(int, raw_input().split())
	print "Case #{}: {}".format(case, solve(patmx, patdig, permx, probs, I, N))
