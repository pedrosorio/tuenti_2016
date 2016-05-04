from collections import defaultdict
from hashlib import md5

def get_tree(N):
	cities = set([])
	vis_cit = set([])
	edges = defaultdict(list) 
	rev = {} 
	for _ in xrange(N-1):
		c1, c2 = raw_input().strip().split()
		cities.add(c1)
		cities.add(c2)
		vis_cit.add(c2)
		edges[c1].append(c2)
		rev[c2] = c1
	root = list(cities - vis_cit)[0]
	hash_tree = {}
	get_hash_tree(root, edges, hash_tree)
	hash_to_node = defaultdict(list)
	for node in sorted(hash_tree.keys(), reverse=True):
		hash_to_node[hash_tree[node]].append(node)
	return root, edges, rev, hash_tree, hash_to_node 

#populates a dictionary from city name to hash where hash is depth + hash of subtree 
def get_hash_tree(root, edges, hash_tree, level=0):
	child_hashes = sorted([get_hash_tree(child, edges, hash_tree, level+1) for child in edges[root]])
	m = md5()
	m.update("|".join(child_hashes))
	hash_tree[root] = str(level) + m.digest()
	return hash_tree[root]

def solve(tree0, tree1):
	root0, edges0, rev0, hash0, hash_to_node0 = tree0
	root1, edges1, rev1, hash1, hash_to_node1 = tree1
	mp = {}
	if hash0[root0] != hash1[root1]:
		return "NO"
	all_nodes = sorted(hash0.keys())
	for node in all_nodes:
		cur_hash = hash0[node]
		node1 = hash_to_node1[cur_hash].pop()
		mp[node] = node1
	return ' '.join([k+'/'+mp[k] for k in sorted(mp.keys())])

N = int(raw_input())
tree0 = get_tree(N)
#plot_tree(tree0)
T = int(raw_input())
for case in xrange(1, T+1):
	tree1 = get_tree(N)
	print "Case #%s: %s" % (str(case), solve(tree0, tree1))
