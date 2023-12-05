# Rania Maharani Narendra
# 2106650222
# Kode Asdos 1

import networkx as nx
import random

def generate_random_tree(num_vertices, num_vertices_bnb, filename):
    # create graph
    tree_dp = nx.Graph()
    tree_bnb = nx.Graph()
    
    # Add nodes/vertices to the graaph
    vertices = list(range(1, num_vertices + 1))
    vertices_bnb = list(range(1, num_vertices_bnb + 1))
    tree_dp.add_nodes_from(vertices)
    tree_bnb.add_nodes_from(vertices_bnb)

    # randomize without root (cause root dont have parents)
    random.shuffle(vertices[1:])
    
    # assign parents (to create edges) except root
    for v in vertices[1:]:
        # randomly add edge between parent and child
        parent = random.randint(1, v-1)
        tree_dp.add_edge(parent, v)
        # for bnb dataset, just add for <= num_vertices_bnb
        if parent <= num_vertices_bnb and v <= num_vertices_bnb:
            tree_bnb.add_edge(parent, v)
            
    # dp  
    with open(filename + "_dp.txt", "w") as file:
        # Write the number of nodes on the first line
        file.write(f"{len(tree_dp)}\n")

        # Write the adjacency list for each node
        tree_dp_arr = nx.to_dict_of_lists(tree_dp)
        for node, neighbors in tree_dp_arr.items():
            line = f"{' '.join(map(str, neighbors))}\n"
            file.write(line)  
       
    # bnb
    with open(filename + "_bnb.txt", "w") as file:
        # Write the number of nodes on the first line
        file.write(f"{len(tree_bnb)}\n")

        # Write the adjacency list for each node
        tree_bnb_arr = nx.to_dict_of_lists(tree_bnb)
        for node, neighbors in tree_bnb_arr.items():
            line = f"{' '.join(map(str, neighbors))}\n"
            file.write(line)

# Example usage with 5 vertices
generate_random_tree(10**4, 60, "small_dataset")
generate_random_tree(10**5, 85, "medium_dataset")
generate_random_tree(10**6, 100, "large_dataset")
