import telnetlib
from collections import deque

def get_screen():
    return [t.read_until('\n') for _ in xrange(7)]

mp = [['u' for j in xrange(1000)] for i in xrange(1000)]
x = y = mnx = mny = mxx = mxy = 500
movs = {'u': [-1,0], 'd': [1,0], 'l': [0,-1], 'r': [0,1]}

def next_movs(mp, y, x, vis):
    nmovs = []
    for char, mov in movs.iteritems():
        ny, nx = y+mov[0], x+mov[1]
        if mp[ny][nx] != '#' and (ny, nx) not in vis:
            nmovs.append(((ny, nx), char))
    return nmovs

# go explore anything that hasn't been visited yet
# previously this would try to reach areas that haven't
# been seen but that would fail to reveal the whole code 
# because it is enclosed by an inner wall
#
# in order to look at the whole code, prioritize visiting
# locations near the wall
# the wall location could be determined dynamically, but 
# I ran the program twice and am trying to optimize for #problems solved
# so I will just hardcode the values 
def bfs_unknown(mp, y, x, all_vis):
    fr = {}
    vis = set([])
    q = deque([(y, x)])
    while q:
        cy, cx = q.popleft()
        for nxt, char in next_movs(mp, cy, cx, vis):
            fr[nxt] = (cy, cx, char)
            vis.add(nxt)
            q.append(nxt)
            ny, nx = nxt
            if mp[ny][nx] == 'u' or (nxt not in all_vis 
                and (ny < 464 or nx < 464 or ny > 536 or nx > 536)):
                orders = []
                # make sure we don't run into walls
                if mp[ny][nx] == 'u':
                    ny, nx, char = fr[(ny, nx)]
                while (ny, nx) != (y, x):
                    ny, nx, char = fr[(ny, nx)]
                    orders.append(char)
                return orders
    return []

def print_to_file(mp, mny, mnx, mxy, mxx, ct):
    with open('mapfile', 'w') as f:
        f.writelines(str(ct)+'\n')
        f.writelines(''.join(map(str, [mny, mnx, mxy, mxx])) + '\n')
        for row in xrange(mny-3, mxy+4):
            f.writelines(''.join(mp[row][mnx-3:mxx+4])+'\n')

t = telnetlib.Telnet("52.49.91.111", 1986)
goal = None
ct = 0
all_vis = set([(y,x)])
while True:
    mny, mxy = min(y, mny), max(y, mxy)
    mnx, mxx = min(x, mnx), max(x, mxx)
    if ct % 300 == 1:
        print_to_file(mp, mny, mnx, mxy, mxx, ct)
    v = get_screen()
    for i in xrange(7):
        for j in xrange(7):
            if i == 3 and j == 3:
                mp[y][x] = ' '
                continue
            mp[y+i-3][x+j-3] = v[i][j]
    print ''.join(v)
    if not goal:
        goal = bfs_unknown(mp, y, x, all_vis)
    if not goal:
        print_to_file(mp, mny, mnx, mxy, mxx, str(ct) + " F YEAH!")
        break
    print goal
    next = goal.pop()
    dy, dx = movs[next]
    y += dy
    x += dx
    all_vis.add((y,x))
    ct += 1
    t.write(next + '\n')

lines = open("mapfile").readlines()[2:]
first_seg = lines[1][5:-2]
second_seg = ''.join([lines[i][-3] for i in xrange(2,len(lines)-1)])
third_seg = lines[-2][-4:0:-1]
fourth_seg = ''.join([lines[i][1] for i in xrange(len(lines)-3, 2, -1)])
print first_seg
print second_seg
print third_seg
print fourth_seg
print ''.join(first_seg+second_seg+third_seg+fourth_seg)
