def solve(N):
	if N == 0:
		return 0
	if N <= 4:
		return 1
	return (N-3)/2 + 1


T = int(raw_input())
for case in xrange(1,T+1):
	N = int(raw_input())
	print "Case #{}: {}".format(case, str(solve(N)))