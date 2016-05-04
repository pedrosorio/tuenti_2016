from collections import Counter

def solve(words, A, B):
	return ','.join(["{} {}".format(w[0], w[1]) 
		for w in Counter(words[A-1:B]).most_common(3)])

	

words = open("corpus.txt").readlines()[0].split()
T = int(raw_input())
for case in xrange(1,T+1):
	A, B = map(int,raw_input().split())
	print "Case #{}: {}".format(case, str(solve(words, A, B)))