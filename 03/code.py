import yaml

# to efficiently prepends items (negative positions in the tape)
# keep two lists
def get_pos(pos):
	if pos >= 0:
		return 0, pos
	else:
		return 1, -pos+1

def solve(tape, code):
	lst = [c for c in tape]
	tape = [lst]
	state = 'start'
	pos = 0
	while state != 'end':
		main_lst, sub_pos = get_pos(pos)
		if sub_pos == len(tape[main_lst]):
			tape[main_lst].append(' ')
		insts = code[state][tape[main_lst][sub_pos]]
		if 'write' in insts:
			tape[main_lst][sub_pos] = insts['write']
		if 'move' in insts:
			m = insts['move']
			if m == 'right':
				pos += 1
			elif m == 'left':
				pos -= 1
		if 'state' in insts:
			state = insts['state']
	return ''.join(lst)


filename = raw_input()
inp = yaml.load('\n'.join(open(filename).readlines()))
for num in inp['tapes']:
	print "Tape #{}: {}".format(num, solve(inp['tapes'][num], inp['code']))