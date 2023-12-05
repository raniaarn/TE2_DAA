# Rania Maharani Narendra
# 2106650222
# Kode Asdos 1

import networkx as nx
import operator
import time, tracemalloc

# parse 
def read_adjacency_list(file_path):
    with open(file_path, "r") as file:
        # Read the number of nodes from the first line
        num_nodes = int(file.readline().strip())

        # Initialize an empty list to store the adjacency list
        adjacency_list = []

        # Read the adjacency list for each node
        for line in file:
            neighbors = list(map(int, line.strip().split()))
            adjacency_list.append(neighbors)

    return adjacency_list, num_nodes

# dynamic programming, code from: https://www.geeksforgeeks.org/vertex-cover-problem-dynamic-programming-solution-for-tree/ 
def dfs(adj, dp, src, par):
    for child in adj[src]:
        if child != par:
            dfs(adj, dp, child, src)
 
    for child in adj[src]:
        if child != par:
            # not including source in the vertex cover
            dp[src][0] = dp[child][1] + dp[src][0]
 
            # including source in the vertex cover
            dp[src][1] = dp[src][1] + min(dp[child][1], dp[child][0])
 
 
def minSizeVertexCover(adj, N):
    dp = [[0 for j in range(2)] for i in range(N+1)]
    for i in range(1, N+1):
        # 0 denotes not included in vertex cover
        dp[i][0] = 0
 
        # 1 denotes included in vertex cover
        dp[i][1] = 1
 
    dfs(adj, dp, 1, -1)
 
    # printing minimum size vertex cover
    print(min(dp[1][0], dp[1][1]))

# BNB, code from: https://github.com/sangyh/minimum-vertex-cover/blob/master/BnB_Edited.py
def parse(datafile):
	adj_list = []
	with open(datafile) as f:
		num_vertices = int(f.readline().strip())
		for i in range(num_vertices):
			adj_list.append(map(int, f.readline().split()))
	return adj_list

def create_graph(adj_list):
	G = nx.Graph()
	for i in range(len(adj_list)):
		for j in adj_list[i]:
			G.add_edge(i + 1, j)
	return G

def BnB(G):
	# INITIALIZE SOLUTION VC SETS AND FRONTIER SET TO EMPTY SET
    OptVC = []
    CurVC = []
    Frontier = []
    neighbor = []

    # ESTABLISH INITIAL UPPER BOUND
    UpperBound = G.number_of_nodes()

    CurG = G.copy()  # make a copy of G
    # sort dictionary of degree of nodes to find node with highest degree
    v = find_maxdeg(CurG)
    #v=(1,0)

    # APPEND (V,1,(parent,state)) and (V,0,(parent,state)) TO FRONTIER
    Frontier.append((v[0], 0, (-1, -1)))  # tuples of node,state,(parent vertex,parent vertex state)
    Frontier.append((v[0], 1, (-1, -1)))
    # print(Frontier)

    while Frontier!=[]:
        (vi,state,parent)=Frontier.pop() #set current node to last element in Frontier
        
        #print('New Iteration(vi,state,parent):', vi, state, parent)
        backtrack = False

        #print(parent[0])
        # print('Neigh',vi,neighbor)
        # print('Remaining no of edges',CurG.number_of_edges())

        
        if state == 0:  # if vi is not selected, state of all neighbors=1
            neighbor = CurG.neighbors(vi)  # store all neighbors of vi
            for node in list(neighbor):
                CurVC.append((node, 1))
                CurG.remove_node(node)  # node is in VC, remove neighbors from CurG
        elif state == 1:  # if vi is selected, state of all neighbors=0
            # print('curg',CurG.nodes())
            CurG.remove_node(vi)  # vi is in VC,remove node from G
            #print('new curG',CurG.edges())
        else:
            pass

        CurVC.append((vi, state))
        CurVC_size = VC_Size(CurVC)
        #print('CurVC Size', CurVC_size)
        # print(CurG.number_of_edges())
        # print(CurG.edges())

        # print('no of edges',CurG.number_of_edges())
        if CurG.number_of_edges() == 0:  # end of exploring, solution found
            #print('In FIRST IF STATEMENT')
            if CurVC_size < UpperBound:
                OptVC = CurVC.copy()
                #print('OPTIMUM:', OptVC)
                UpperBound = CurVC_size
                #print('New VC:',OptVC)
            backtrack = True
            #print('First backtrack-vertex-',vi)
                
        else:   #partial solution
            #maxnode, maxdegree = find_maxdeg(CurG)
            CurLB = Lowerbound(CurG) + CurVC_size
            #print(CurLB)
            #CurLB=297

            if CurLB < UpperBound:  # worth exploring
                # print('upper',UpperBound)
                vj = find_maxdeg(CurG) # ini gak sihh
                Frontier.append((vj[0], 0, (vi, state)))#(vi,state) is parent of vj
                Frontier.append((vj[0], 1, (vi, state)))
                # print('Frontier',Frontier)
            else:
                # end of path, will result in worse solution,backtrack to parent
                backtrack=True
                #print('Second backtrack-vertex-',vi)


        if backtrack==True:
            #print('Hello. CurNode:',vi,state)
            if Frontier != []:	#otherwise no more candidates to process
                nextnode_parent = Frontier[-1][2]	#parent of last element in Frontier (tuple of (vertex,state))
                #print(nextnode_parent)

                # backtrack to the level of nextnode_parent
                if nextnode_parent in CurVC:
                    
                    id = CurVC.index(nextnode_parent) + 1
                    while id < len(CurVC):	#undo changes from end of CurVC back up to parent node
                        mynode, mystate = CurVC.pop()	#undo the addition to CurVC
                        CurG.add_node(mynode)	#undo the deletion from CurG
                        
                        # find all the edges connected to vi in Graph G
                        # or the edges that connected to the nodes that not in current VC set.
                        
                        curVC_nodes = list(map(lambda t:t[0], CurVC))
                        for nd in G.neighbors(mynode):
                            if (nd in CurG.nodes()) and (nd not in curVC_nodes):
                                CurG.add_edge(nd, mynode)	#this adds edges of vi back to CurG that were possibly deleted

                elif nextnode_parent == (-1, -1):
                    # backtrack to the root node
                    CurVC.clear()
                    CurG = G.copy()
                else:
                    print('error in backtracking step')

    return OptVC

#TO FIND THE VERTEX WITH MAXIMUM DEGREE IN REMAINING GRAPH
def find_maxdeg(g):
	deglist = g.degree()
	deglist_sorted = sorted(deglist, reverse=True, key=operator.itemgetter(
		1))  # sort in descending order of node degree
	v = deglist_sorted[0]  # tuple - (node,degree)
	return v

#EXTIMATE LOWERBOUND
def Lowerbound(graph):
	lb=graph.number_of_edges() / find_maxdeg(graph)[1]
	lb=ceil(lb)
	return lb

def ceil(d):
    """
        return the minimum integer that is bigger than d
    """ 
    if d > int(d):
        return int(d) + 1
    else:
        return int(d)
    
#CALCULATE SIZE OF VERTEX COVER (NUMBER OF NODES WITH STATE=1)
def VC_Size(VC):
	# VC is a tuple list, where each tuple = (node_ID, state, (node_ID, state)) vc_size is the number of nodes which has state == 1
	vc_size = 0
	for element in VC:
		vc_size = vc_size + element[1]
	return vc_size

def run_dp(cond_dp, input_dp):
    print(f"================={cond_dp} DP================")
    # preparing input
    adj, N = read_adjacency_list(input_dp)
    adj.insert(0, [])
    
    # start count time
    tracemalloc.start()
    start = time.time()
    minSizeVertexCover(adj, N)
    end = time.time()
    memory_stats_dp = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    
    # output
    print(f"time executed for DP: {str((end-start)* 1000)} milliseconds")
    print(f"memory usage: {memory_stats_dp[1] / 10**6} MB")
    
def run_bnb(cond_bnb, input_bnb):
    print(f"================={cond_bnb} BNB================")
    # preparing input
    adj = parse(input_bnb)
    g = create_graph(adj)
    
    # start count time
    tracemalloc.start()
    start = time.time()
    Sol_VC = BnB(g)
    end = time.time()
    memory_stats_bnb = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    
    # delete false nodes and print output
    for element in Sol_VC:
        if element[1]==0:
            Sol_VC.remove(element)
    print(len(Sol_VC))
    
    # output
    print(f"time executed for BNB: {str((end-start)* 1000)} milliseconds")
    print(f"memory usage: {memory_stats_bnb[1] / 10**6} MB")
    
# dataset
run_dp("10^4 Vertices", "small_dataset_dp.txt")
run_bnb("60 Vertices", "small_dataset_bnb.txt")

run_dp("10^5 Vertices", "medium_dataset_dp.txt")
run_bnb("80 Vertices", "medium_dataset_bnb.txt")

run_dp("10^6 Vertices", "large_dataset_dp.txt")
run_bnb("100 Vertices", "large_dataset_bnb.txt")
