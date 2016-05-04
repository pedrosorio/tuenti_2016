
#If a city with the original virus (ai) has more than one equivalent from the cities with another virus (bj and bk where bj < bk), 
#it will be related to the first city according to alphabetical order: (ai/bj)
from collections import defaultdict
from hashlib import md5
#import pydot

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
	return root, edges, rev, hash_tree 

def get_hash_tree(root, edges, hash_tree):
	child_hashes = sorted([get_hash_tree(child, edges, hash_tree) for child in edges[root]])
	m = md5()
	m.update("|".join(child_hashes))
	hash_tree[root] = m.digest()
	return hash_tree[root]

def solve(tree0, tree1):
	root0, edges0, rev0, hash0 = tree0
	root1, edges1, rev1, hash1 = tree1
	mp = {root0: root1}
	rmp = {root1: root0}
	if hash0[root0] != hash1[root1]:
		return "NO"
	all_nodes = sorted([root0] + [v for lst in edges0.values() for v in lst])
	for ori in all_nodes: 
		if ori in mp:
			continue
		par_lst = []
		par = ori
		while par not in mp:
			par_lst.append(par)
			par = rev0[par]
		possible1 = [mp[par]]
		while par_lst:
			par = par_lst.pop()
			nxt_hash = hash0[par]
			possible1 = [nxt1 for pos in possible1 for nxt1 in edges1[pos] if nxt1 not in rmp and hash1[nxt1] == nxt_hash]
		chosen = min(possible1)
		mp[ori] = chosen
		rmp[chosen] = ori
		while ori not in mp:
			ori = rev0[ori]
			chosen = rev1[chosen]
			mp[ori] = chosen
			rmp[chosen] = ori
	return ' '.join([k+'/'+mp[k] for k in sorted(mp.keys())])

"""
def plot_tree(tree, name = 'graph.png'):
	graph = pydot.Dot(graph_type='graph')
	root, edges = tree[:2]
	all_nodes = [root] + [v for lst in edges.values() for v in lst]
	graph_nodes = {}
	for node in all_nodes:
		graph_nodes[node] = pydot.Node(node, label=node)
		graph.add_node(graph_nodes[node])
	for k in edges.keys():
		for d in edges[k]:
			graph.add_edge(pydot.Edge(graph_nodes[k], graph_nodes[d]))
	graph.write_png(name)
"""

N = int(raw_input())
tree0 = get_tree(N)
#plot_tree(tree0)
T = int(raw_input())
for case in xrange(1, T+1):
	tree1 = get_tree(N)
	"""
	if case == 3:
		plot_tree(tree1, name = 'graph3.png')
	"""
	print "Case #%s: %s" % (str(case), solve(tree0, tree1))
