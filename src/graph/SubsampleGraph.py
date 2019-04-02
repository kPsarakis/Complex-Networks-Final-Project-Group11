import networkx as nx

def random_connected_node_selection(graph, N):
    # Select a random node from the nodelist and add it to the set
    pass

# @TODO: Change into random node set returned (and make a seperate method for constructing the graph)
def random_subample(graph, N):
    # Select a random node from the nodelist and add it to the set
    current_nodes = set()
    outermost_nbs = set()
    new_outermost_nbs = set()

    while True:
        for n in outermost_nbs:
            # Fetch outgoing edges from this node
            nbs = G.adj[n]

            # Add all to new neighbours.
            new_outermost_nbs.union(nbs)

            # Extend sets
            # current_nodes.

            if len(current_nodes) > N:
                break;

        outermost_nbs = new_outermost_nbs

        if len(outermost_nbs) == 0:
            print("Fully explored connected component")
            break;

    # Conststruct subgraph from current_nodes

    pass


# @TODO: Rename
def random_subsample_2():
    # Perform random_subsample(), if it doesn't match, then remove all these nodes from the graph
    pass