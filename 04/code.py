combos = [['L', 'LD', 'D', 'RD', 'R', 'P'], ['D', 'RD', 'R', 'P'], ['R', 'D', 'RD', 'P'], ['D', 'LD', 'L', 'K'], ['R', 'RD', 'D', 'LD', 'L', 'K']]

def solve(moves):
	# treat each combo as a FSM and check how many times does it end with a failure in the last move
	ct = 0
	C = len(combos)
	fsm_pos = [0 for _ in xrange(C)]
	for move in moves:
		# can fail at most one combo
		failed_combo = False	
		for c in xrange(C):
			if move == combos[c][fsm_pos[c]]:
				fsm_pos[c] += 1
				# performed the combo, reset this combo
				# it is not clear from the statement whether performing a combo resets all other combos,
				# assuming that's the case
				if fsm_pos[c] == len(combos[c]):
					fsm_pos = [0 for _ in xrange(C)]
					break
			else:
				if fsm_pos[c] == len(combos[c]) - 1:
					if not failed_combo:
						ct += 1
						failed_combo = True
				fsm_pos[c] = 0
				if combos[c][0] == move:
					fsm_pos[c] = 1
	return ct

N = int(raw_input())
for case in xrange(1, N+1):
	moves = raw_input().split('-') + ['']
	print "Case #{}: {}".format(case, solve(moves))
