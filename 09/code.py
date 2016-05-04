# find smallest k such that 10^k % (9v) == 1, i.e. (10^k - 1)/9 = 1111...111 (k times)
def get_ones(v):
    mod = 9*v
    k = 1
    r = 10 % mod
    while r != 1:
        r = (r*10) % mod
        k += 1
    return k

def solve(N):
    ct5, ct2 = 0, 0
    while N%2 == 0:
        N /= 2
        ct2 += 1
    while N%5 == 0:
        N /= 5
        ct5 += 1
    zeros = max(ct2, ct5)
    ones = get_ones(N)
    return "{} {}".format(ones, zeros)


C = int(raw_input())
for case in xrange(1, C+1):
    N = int(raw_input())
    print "Case #{}: {}".format(case, solve(N))