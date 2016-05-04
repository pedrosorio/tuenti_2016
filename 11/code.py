def get_bits(n):
	bit = 0
	bits = []
	while n > 0:
		if n & 1:
			bits.append(bit)
		n >>= 1
		bit += 1
	return bits

# solve assuming n piles of 1 trying to get k
def sub_solve(n, k):
	if n > k:
		return "IMPOSSIBLE" 
	if n == k:
		return 0
	k -= n-1
	bits = get_bits(k)
	return bits[-1] + len(bits) - 1

def solve(n, m, k):
	if k%m != 0 or k < n*m:
		return "IMPOSSIBLE"
	if k == n*m:
		return 0
	mult = k/m
	return sub_solve(n, mult)
	
C = int(raw_input())
for case in xrange(1, C+1):
	N, M, K = map(int, raw_input().split())
	print "Case #{}: {}".format(case, solve(N, M, K))